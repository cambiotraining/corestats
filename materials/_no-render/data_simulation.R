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

## Two-way ANOVA ----

exercise <- read_csv("materials/data/CS4-exercise.csv")

exercise %>%
    group_by(sex, exercise) %>%
    summarise(mean = mean(weight),
              sd = sd(weight))

# make this reproducible
set.seed(1638)

female_control <- tibble(sex = "female", exercise = "control",
                         weight = rnorm(41, 74.9, 4.27))
female_runner <- tibble(sex = "female", exercise = "runner",
                        weight = rnorm(36, 64.8, 3.91))
male_control <- tibble(sex = "male", exercise = "control",
                          weight = rnorm(42, 81.9, 3.23))
male_runner <- tibble(sex = "male", exercise = "runner",
                      weight = rnorm(41, 79.9, 3.51))

exercise <- bind_rows(female_control, female_runner, male_control, male_runner)

write_csv(exercise, "materials/data/CS4-exercise.csv")

exercise %>%
    ggplot(aes(exercise, weight, colour = sex, group = sex)) +
    geom_jitter(width = 0.05) +
    stat_summary(fun = mean, geom = "point", size = 3) +
    stat_summary(fun = mean, geom = "line") +
    scale_colour_brewer(palette = "Dark2")

lm_exercise <- lm(weight ~ exercise * sex, data = exercise)

lm_exercise %>%
    resid_panel(plots = c("resid", "qq", "ls", "cookd"),
                smoother = TRUE)

age <- rnorm(183, 52, 4)
#weight <- rnorm(183, 75, 6)
#sys_bp <- rnorm(183, 135, 5)
e <- rnorm(183, 0, 8)
e2 <- abs(rnorm(183, 1, 0.2))
sex <- round(runif(183, min = 0, max = 1))
exercise <- round(runif(183, min = 0, max = 1))

beta0 <- 74.22
beta1 <- -4.14
beta2 <- 3.96
beta3 <- 8.27
beta4 <- 0.23

weight <- beta0 + (beta1*exercise) + (beta2*sex) + (beta3*exercise*sex) + e
sys_bp <- rnorm(183, 135, 2) * (weight * e2)

data <- tibble(age = age,
       weight = weight,
       sys_bp = sys_bp,
       exercise = exercise,
       sex = sex)

example <- data %>%
    mutate(exercise = if_else(exercise == 0, "control", "runner"),
           sex = if_else(sex == 0, "female", "male"))

example %>% select(weight) %>% min()

example %>%
    select(where(is.numeric)) %>%
    pairs()

example %>% select(sys_bp) %>% max()

example %>%
    count(exercise, sex)

example %>%
    ggplot(aes(sys_bp, weight, colour = sex)) +
    geom_point()


anova(lm(weight ~ sex * exercise,
   data = example))

anova(lm(sys_bp ~ weight,
         data = example))

example %>%
    ggplot(aes(exercise, weight, colour = sex, group = sex)) +
    geom_point() +
    stat_summary(fun = mean, geom = "point", size = 3) +
    stat_summary(fun = mean, geom = "line")

example %>%
    ggplot(aes(x = sex, y = weight, fill = exercise)) +
    geom_boxplot() +
    scale_fill_brewer(palette = "Dark2")

example %>%
    ggplot(aes(x = sex,
               y = weight,
               colour = exercise, group = exercise)) +
    geom_point() +
    stat_summary(fun = mean, geom = "point", size = 3) +
    stat_summary(fun = mean, geom = "line") +
    scale_colour_brewer(palette = "Dark2")

# define the linear model
lm_example <- lm(weight ~ sex + exercise,
                  data = example)

lm_example %>%
    resid_panel(plots = c("resid", "qq", "ls", "cookd"),
                smoother = TRUE)

example %>% select(age) %>% plot()

## Cells replacement ----

cells <- read_csv("materials/data/CS4-cells.csv")

cells %>%
    rename(genotype = cell_type,
           plant_height = cell_number) %>%
    mutate(genotype = if_else(genotype == "A",  "control", "mutant")) %>%
    group_by(genotype, concentration) %>%
    summarise(mean = mean(plant_height),
              sd = sd(plant_height))

set.seed(7231)
control_high <- tibble(genotype = "control", concentration = "high",
                         plant_height = rnorm(34, 31, 3.62))

control_low <- tibble(genotype = "control", concentration = "low",
                       plant_height = rnorm(43, 38, 3.67))

control_none <- tibble(genotype = "control", concentration = "none",
                       plant_height = rnorm(56, 45, 2.47))

mutant_high <- tibble(genotype = "mutant", concentration = "high",
                      plant_height = rnorm(47, 35, 2.09))

mutant_low <- tibble(genotype = "mutant", concentration = "low",
                      plant_height = rnorm(43, 37, 3.06))

mutant_none <- tibble(genotype = "mutant", concentration = "none",
                       plant_height = rnorm(52, 40, 2.27))

auxin_response <- bind_rows(control_high, control_low, control_none,
          mutant_high, mutant_low, mutant_none)

auxin_response <- auxin_response %>%
    mutate(plant_height = round(plant_height, 1))

ggplot(auxin_response, aes(concentration, plant_height, colour = genotype, group = genotype)) +
    geom_jitter(width = 0.05) +
    stat_summary(fun = mean, geom = "point", size = 3) +
    stat_summary(fun = mean, geom = "line") +
    scale_colour_brewer(palette = "Dark2")

ggplot(auxin_response, aes(genotype, plant_height, colour = concentration, group = concentration)) +
    stat_summary(fun = mean, geom = "point", size = 3) +
    stat_summary(fun = mean, geom = "line") +
    scale_colour_brewer(palette = "Dark2")

lm_auxin <- lm(plant_height ~ genotype * concentration,
               data = auxin_response)

lm_auxin %>%
    resid_panel(plots = c("resid", "qq", "ls", "cookd"),
                smoother = TRUE)

lm_auxin %>% resid() %>% shapiro_test()
anova(lm_auxin)

write_csv(auxin_response, "materials/data/CS4-auxin.csv")

## CS5 data ----

h2s <- read_csv("materials/data/CS5-H2S.csv")

h2s %>%
    group_by(treatment_plant) %>%
    get_summary_stats()

set.seed(271)
inner_london <- tibble(inner = rgamma(365, 15.6, 2.62) + 8) %>%
    mutate(id = 1:n())

ggplot(inner_london, aes(id, inner)) +
    geom_point()

outer_london <- tibble(outer = rgamma(365, 11.4, 3.81) + 6) %>%
    mutate(id = 1:n())

ggplot(outer_london, aes(id, outer)) +
    geom_point()

london <- left_join(inner_london, outer_london, by = "id")


# read in weather data
weather_data <- read_csv("materials/_no-render/heathrow_weather_2019.csv")

# add some jitter to the wind speed
weather_data <- weather_data %>%
    mutate(wind_m_s = jitter(wind_m_s, factor = 2, amount = 0.3))

london_airquality <- weather_data %>%
    mutate(id = 1:n()) %>%
    left_join(london, by = "id") %>%
    rename(inner_pm2_5 = inner,
           outer_pm2_5 = outer)

london_airquality %>%
    pivot_longer(cols = c(inner_pm2_5, outer_pm2_5),
                 names_to = "location",
                 values_to = "pm2_5") %>%
    ggplot(aes(location, pm2_5)) +
    geom_boxplot() +
    geom_jitter(width = 0.1)

london_airquality %>%
    pivot_longer(cols = c(inner_pm2_5, outer_pm2_5),
                 names_to = "location",
                 values_to = "pm2_5") %>%
    ggplot(aes(wind_m_s, pm2_5, colour = location)) +
    geom_point() +
    geom_smooth(method = "lm", se = FALSE)

london_airquality %>%
    pivot_longer(cols = c(inner_pm2_5, outer_pm2_5),
                 names_to = "location",
                 values_to = "pm2_5") %>%
    lm(pm2_5 ~ avg_temp * location, data = .) %>%
    anova()


