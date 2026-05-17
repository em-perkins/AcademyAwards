AcademyAwards_v2
================
Emely P.
2026-04-02

## Install library

``` r
library(readr)
library(dplyr)
```

    ## 
    ## Attaching package: 'dplyr'

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

``` r
library(tidyr)
library(stringr)
```

\##Read csv

``` r
AA <- read_csv("~/Downloads/AA.csv")
```

    ## Rows: 1141 Columns: 2
    ## ── Column specification ────────────────────────────────────────────────────────
    ## Delimiter: ","
    ## chr (2): Winner, Column2
    ## 
    ## ℹ Use `spec()` to retrieve the full column specification for this data.
    ## ℹ Specify the column types or set `show_col_types = FALSE` to quiet this message.

\##Extract Year and Session

``` r
AA <- AA %>%
  mutate(
    Ceremony_Year = str_extract(Column2, "^\\d{4}"),
    Session = str_extract(Column2, "(?<=\\()\\d+")
  ) %>%
  fill(Ceremony_Year, Session)
```

## Rename Winner column

``` r
AA <- AA %>%
  rename(
    Award_Status = Winner)
```

## Extract Category

``` r
AA <- AA %>%
  mutate(
    Category = if_else(
      is.na(Award_Status) & !str_detect(Column2, "^\\d{4}"),
      Column2,
      NA_character_
    )
  ) %>%
  fill(Category)
```

\##Keep winner and nominee

``` r
AA_clean <- AA %>%
  filter(!is.na(Award_Status))
```

## Extract nominee, film, and role

``` r
AA_clean <- AA_clean %>%
  mutate(
    Nominee = str_extract(Column2, "^[^\\-]+") %>% str_trim(),
    Film = str_extract(Column2, "(?<=-- ).+?(?= \\{)"),
    Role = str_extract(Column2, "(?<=\\{\").+?(?=\"\\})")
  )
```

## Final dataset

``` r
AA_final <- AA_clean %>%
  select(
    Award_Status,
    Ceremony_Year,
    Session,
    Category,
    Nominee,
    Film,
    Role
  )
```

\##Download final dataset as csv

``` r
write_csv(AA_final, "AA_final.csv")
```
