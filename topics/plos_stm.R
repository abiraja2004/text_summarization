require(magrittr)
require(dplyr)
require(quanteda)
require(tidyr)
require(stm)
require(lubridate)
require(stmCorrViz)
require(LDAvis)

setwd("/home/psh/Documents/NIS")

data <- readRDS("plos_med_articles") %>%
  distinct(
    id,
    publication_date,
    title,
    abstract,
    introduction,
    results_and_discussion,
    materials_and_methods
  ) %>%
  mutate(publication_date = parse_date_time(publication_date, "YmdHMS")) %>%
  gather(section, text, -id, -publication_date) %>%
  group_by(id) %>%
  filter(all(text != "none")) %>%
  ungroup() %>%
  mutate_each(funs(factor), id, section) %>%
  mutate(int_date = as.integer(publication_date))

model <- data %$%
  dfm(text, stem = TRUE, ignoredFeatures = stopwords()) %>%
  trim(minDoc = 15) %>%
  convert("tm") %>%
  readCorpus(type = "slam") %$%
  stm(
    documents,
    vocab,
    K = 100,
    prevalence = ~ s(int_date) + section,
    data = data,
    interactions = FALSE,
    max.em.its = 50,
    ngroups = 20
  )

stmCorrViz(
  model,
  file_out = "corrviz.html",
  documents_matrix = docs$documents,
  documents_raw = data$text
)

toLDAvis(model, docs) %>% 
  serVis(out.dir = "~/Documents/NIS/ldaviz/")

require(ggplot2)
require(plotly)
require(proxy)

query <- "10.1371/journal.pone.0163569"

data$vec <- split(model$theta, 1:nrow(model$theta))

data %<>% group_by(section) %>%
  mutate(sim = as.numeric(proxy::simil(Reduce(rbind, vec), t(vec[[which(id == query)]]))), method = "fJaccard") %>%
  ungroup() %>% 
  group_by(id) %>%
  mutate(title = text[section == "title"]) %>%
  ungroup()

data %>% 
  filter(section != "title", sim > 0.8) %>% 
  ggplot(aes(publication_date, sim)) + 
  geom_point(data = data %>% filter(id == query, section != "title"), color = "red", size = 3) +
  geom_point(aes(color = sim, text = title)) +
  facet_grid(section ~ .) +
  theme_light() + 
  guides(color = FALSE)

ggplotly()


