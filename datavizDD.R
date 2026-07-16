install.packages("tidytext")
install.packages("stringr")
install.packages("tidyr")

library(arrow)
library(dplyr)
library(ggplot2)
library(scales)
library(tidytext)
library(stringr)

df <- read_parquet("train-00000-of-00001.parquet")
head(df)

# MeAJOR Corpus Dataset — Data Visualization 
# Phishing Email Classifier Project (4ALL)

#  1. Bar chart: does the email contain a URL / an attachment? 

df <- df %>%
  filter(!is.na(label)) %>%
  mutate(
    label_f = factor(label, levels = c(0, 1), labels = c("Legitimate", "Phishing")),
    doc_id = row_number()
  )

cat("Rows after cleaning:", nrow(df), "\n")

# Visualization 1
# Bar chart: % of emails containing a URL vs. an attachment, by label
# url_count` and has_attachments = are the two columns that
# describe actual email CONTENT (not metadata like sender/date).

presence_summary <- df %>%
  mutate(has_url = url_count > 0) %>%
  group_by(label_f) %>%
  summarise(
    `Contains a URL` = mean(has_url, na.rm = TRUE) * 100,
    `Contains an attachment` = mean(has_attachments, na.rm = TRUE) * 100
  ) %>%
  tidyr::pivot_longer(-label_f, names_to = "feature", values_to = "pct")

print(presence_summary)

p1 <- ggplot(presence_summary, aes(x = feature, y = pct, fill = label_f)) +
  geom_col(position = position_dodge(width = 0.7), width = 0.6) +
  geom_text(
    aes(label = paste0(round(pct, 1), "%")),
    position = position_dodge(width = 0.7),
    vjust = -0.4,
    size = 4
  ) +
  scale_y_continuous(limits = c(0, 90), expand = expansion(mult = c(0, 0.1))) +
  scale_fill_manual(values = c("Legitimate" = "#2E7D32", "Phishing" = "#C62828")) +
  labs(
    title = "Phishing emails rely on links, not attachments",
    subtitle = "Share of emails containing each feature, by label",
    x = NULL, y = "% of emails", fill = "Label"
  ) +
  theme_minimal(base_size = 13) +
  theme(plot.title = element_text(face = "bold"), panel.grid.major.x = element_blank())

print(p1)
ggsave("viz1_url_attachment_bars.png", p1, width = 7.5, height = 5, dpi = 300)


# Visualization 2
# Pie chart: email format (plain text / HTML / both), by label

# content_types records every MIME part of the email (e.g. an
# email can be "text/plain", "text/html", or both if it has an
# HTML version and a plain-text fallback, which is normal for
# real email clients). Collapse the many combinations in
# the column down to three simple buckets so the pattern is easy to read.

format_summary <- df %>%
  mutate(
    format_simple = case_when(
      is.na(content_types) ~ "Unknown",
      str_detect(content_types, "text/html") & str_detect(content_types, "text/plain") ~ "Both (HTML + plain text)",
      str_detect(content_types, "text/html") ~ "HTML only",
      str_detect(content_types, "text/plain") ~ "Plain text only",
      TRUE ~ "Other"
    ),
    format_simple = factor(
      format_simple,
      levels = c("Plain text only", "Both (HTML + plain text)", "HTML only", "Other", "Unknown")
    )
  ) %>%
  count(label_f, format_simple) %>%
  group_by(label_f) %>%
  mutate(pct = n / sum(n) * 100) %>%
  ungroup()

print(format_summary)

p2 <- ggplot(format_summary, aes(x = "", y = pct, fill = format_simple)) +
  geom_col(width = 1, color = "white") +
  coord_polar(theta = "y") +
  facet_wrap(~ label_f) +
  geom_text(
    aes(label = ifelse(pct >= 3, paste0(round(pct), "%"), "")),
    position = position_stack(vjust = 0.5),
    color = "white",
    fontface = "bold",
    size = 4
  ) +
  scale_fill_manual(values = c(
    "Plain text only"          = "#2E7D32",
    "Both (HTML + plain text)" = "#F9A825",
    "HTML only"                = "#C62828",
    "Other"                    = "#9E9E9E",
    "Unknown"                  = "#616161"
  )) +
  labs(
    title = "Legitimate mail is almost all plain text -- phishing isn't",
    subtitle = "Email format composition, by label",
    fill = "Email format"
  ) +
  theme_void(base_size = 13) +
  theme(
    plot.title = element_text(face = "bold", hjust = 0.5),
    plot.subtitle = element_text(hjust = 0.5),
    strip.text = element_text(face = "bold", size = 13),
    legend.position = "bottom"
  )

print(p2)
ggsave("viz2_content_format_pie.png", p2, width = 8, height = 5.5, dpi = 300)
