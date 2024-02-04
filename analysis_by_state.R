library(tidyverse)
library(ggplot2)

df <-readr::read_csv('names_and_births_2022.csv')
df <- df %>% filter(!Race %in% c("Not Available","Not Reported","Unknown or Not Stated"))
df <- df %>% select(-c("State Code"))
df <- df %>% filter(Count>0)
rose_df <- df %>% filter(Name=='Jamar' & Gender=="M") 
sum_df <- rose_df %>% group_by(Gender) %>% summarise(
  Births=sum(Births),Count=sum(Count),Year=Year,Race="All",Name=Name, State="All"
) %>% distinct()

#rose_df <- rbind(rose_df,sum_df)


lm0 <- lm(Count ~ Births, data=rose_df)
rsq0 <- summary(lm0)$r.squared


m1 <- lm(Count ~ Births, data=rose_df %>% filter(Race=="Asian"))
rsq1 <- summary(lm1)$r.squared

lm2<- lm(Count ~ Births, data=rose_df %>% filter(Race=="White"))
rsq2 <- summary(lm2)$r.squared

lm3<- lm(Count ~ Births, data=rose_df %>% filter(Race=="Black or African American"))
rsq3 <- summary(lm3)$r.squared


p<- ggplot(rose_df,aes(x=Births,y=Count)) + geom_point(aes(color=Race)) + 
             stat_smooth(aes(color=Race), method=lm, se=F)

p


