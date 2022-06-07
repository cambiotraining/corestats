# CS1 Revision exercise ----

# load the data
DrugData <- read.csv("data/examples/cs2-RevisionDrugs.csv")

# visualise the data
boxplot(Value ~ Drug,
        data = DrugData,
        xlab = "Drug Type", ylab = "Value", col = c("lightblue" , "gold"))

# check distribution of drug A data
shapiro.test(unstack(DrugData, Value ~ Drug)$A)
# check distribution of drug B data
shapiro.test(unstack(DrugData, Value ~ Drug)$B)
# check if the variances are equal
bartlett.test(Value~Drug , data=DrugData)

# perform test
t.test(Value ~ Drug,
       data = DrugData, var.equal = TRUE )

# if using diagnostic plots
par(mfrow=c(1,2))?
qqnorm(unstack(DrugData, Value ~ Drug)$A, main = "Drug A")
qqline(unstack(DrugData, Value ~ Drug)$A, col = "red")

qqnorm(unstack(DrugData, Value ~ Drug)$B, main = "Drug B")
qqline(unstack(DrugData, Value ~ Drug)$B, col = "red")
