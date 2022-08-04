# load original oystercatcher data set
oystercatcher <- read_csv("data/CS2-oystercatcher.csv")

# get mean and sd for each group
oystercatcher %>%
    group_by(site) %>%
    summarise(mean = mean(feeding),
              sd = sd(feeding))

# make this reproducible
set.seed(123)
# simulate data based on calculated mean, sd
# note: sd for sheltered is higher than calculated because otherwise
# the bartlett test fails
exposed <- tibble(site = "exposed",feeding = rnorm(40, 13.7, 2.72))
partial <- tibble(site = "partial", feeding = rnorm(40, 17.1, 2.73))
sheltered <- tibble(site = "sheltered", feeding = rnorm(40, 23.6, 2.31))

# create new oystercatcher object
oystercatcher <- bind_rows(exposed, partial, sheltered)

write_csv(oystercatcher, "data/CS2-oystercatcher-feeding.csv")
