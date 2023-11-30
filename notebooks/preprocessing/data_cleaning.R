library(readr)
library(dplyr)

election_dates <- rev(c("2025-01-01", "2019-12-12", "2017-06-08", "2015-05-07", "2010-05-06", "2005-05-05", "2001-06-07",
  "1997-05-01", "1992-04-09", "1987-06-11", "1983-06-09"))

age = read_csv("2011_2021_census_data_age_group.csv")
living = read_csv("2011_2021_census_data_livingstatus.csv")
ethnicity = read_csv("2011_2021_census_data_ethnicity.csv")

age_cleaned = age %>% dplyr::select(c("Age group", "ConstituencyName", "ONSConstID", "RegionName", "Date", "Const%")) %>%
  magrittr::set_colnames(c("Age", "Constituency", "ONSConstID", "RegionName", "Year", "Percentage")) %>%
  mutate(Year = as.integer(Year)) %>%
  mutate(Percentage = as.numeric(substr(Percentage,1,nchar(Percentage)-1))/100) %>%
  tidyr::spread(Age, Percentage)

living_cleaned = living %>% dplyr::select(c("ConstituencyName", "ONSConstID", "groups", "con_num", "con_2011_num")) %>%
  magrittr::set_colnames(c("Constituency", "ONSConstID", "group", "2011", "2021")) %>%
  tidyr::gather("Year", "N_housing", 4:5) %>%
  group_by(Constituency, Year) %>%
  mutate(p_housing = N_housing/sum(N_housing)) %>%
  select(-N_housing) %>%
  tidyr::spread(group, p_housing) %>%
  rename_all(~ gsub(" ", "_", .))

ethnicity_cleaned = ethnicity %>% dplyr::select("ConstituencyName", "ONSConstID", "broad_ethnic_groups", "con_pc_2021", "con_pc_2011") %>%
  magrittr::set_colnames(c("Constituency", "ONSConstID", "group", "2011", "2021")) %>%
  mutate(group = ifelse(group == "Mixed or Multiple ethnic groups", "Mixed", group)) %>%
  tidyr::gather("Year", "Percentage", 4:5) %>%
  tidyr::spread(group, Percentage)


interpolateDataFrame <- function(df, year_start, year_end, start_col=4){
  years_sequence <- seq(year_start, year_end)

  for(cons in unique(df$Constituency)){
    df_filtered = df %>% filter(Constituency==cons)

    interpolated_df <- data.frame(Constituency = cons,
               ONSConstID = df_filtered$ONSConstID[1],
               year = years_sequence)

    for (col in start_col:ncol(df_filtered)) {
      interpolated_values <- approx(df_filtered$Year, df_filtered[[col]], years_sequence, rule=2)$y
      interpolated_df[colnames(df_filtered)[col]] <- interpolated_values
    }

    if (cons==unique(df$Constituency)[1]) interpolated_df_hold <- interpolated_df
    else interpolated_df_hold <- rbind(interpolated_df_hold, interpolated_df)
  }

  return(interpolated_df_hold)
}

# Interpolate stuff
age_interpolated <- interpolateDataFrame(df=age_cleaned, year_start=2010, year_end=2021, start_col=5)
living_interpolated <- interpolateDataFrame(living_cleaned, 2010, 2021)
ethnicity_interpolated <- interpolateDataFrame(ethnicity_cleaned, 2010, 2021)

# Combine everything
combined = left_join(living_interpolated, age_interpolated, by=c("Constituency", "ONSConstID", "year")) %>%
  left_join(., ethnicity_interpolated, by=c("Constituency", "ONSConstID", "year"))



# Polling data
polling = read_csv("monthly_polling_data.csv")

library(zoo)

polling_cleaned = polling %>%
  mutate(Year = zoo::na.locf(Year)) %>%
  dplyr::select(c("Year", "Month", "Conservative", "Labour", "LD")) %>%
  filter(is.na(Conservative)==FALSE) %>%
  filter(Month != "GE") %>%
  mutate(Month = as.Date(ifelse(lag(Month)=="GE", paste("01", Month), paste("28", Month)), format = "%d %b-%y")) %>%
  rowwise() %>%
  mutate(next_election=lubridate::year(election_dates[which(election_dates>Month)][1])) %>%
  tidyr::gather("Party", "Score", 3:5) %>%
  group_by(Party, next_election)

summary1 = polling_cleaned %>%
  filter(is.na(Month)==F) %>%
  summarise(min = min(Score), max=max(Score), average=mean(Score))

summary2 = polling_cleaned %>%
  slice_max(order_by = Month) %>%
  dplyr::select(Party, next_election, Score) %>%
  magrittr::set_colnames(c("Party", "next_election", "Pre_GE_poll"))

polling_summary = left_join(summary1, summary2, by=c("Party", "next_election")) %>%
  tidyr::gather(metric, value, 3:6) %>%
  mutate(value = value/100) %>%
  mutate(concat = paste0(Party,"_",metric)) %>% ungroup() %>%
  select(-metric, -Party) %>%
  tidyr::spread(concat, value) %>%
  dplyr::rename(election=next_election)







X_init = combined %>% filter(year %in% unique(polling_summary$election)) %>%
  left_join(., polling_summary, by=c("year" = "election"))

ref_list = living_cleaned  %>% group_by(Constituency, ONSConstID, Year) %>% filter(row_number()==1) %>% select(c("Year", "Constituency", "ONSConstID"))
write.csv(ref_list, "ref_list.csv")

election_data = read_csv("cleaned_elections_data_with_incumbent.csv")

X_init %>% nrow()
election_data %>% nrow()

full_df = left_join(X_init, election_data, by=c("ONSConstID"="constituency_id", "year"))
write.csv(full_df, "full_df.csv")
