# JobDash

## Business Understanding
The job market for the data industry can be difficult to navigate because there are a plethora of job titles and the relationship between titles and roles is often not well defined.
Two identical roles may have completely different titles.
Two substantially different roles may have the same title.
This limits the usability of job titles as a means to succinctly communicate about data industry jobs.
This project will address the issue by directly analyzing full job descriptions from a corpus of job postings to provide three main deliverables.
 * First, from the language used in job descriptions (without titles), identify new clusters of similar jobs based on their roles and responsibilities.
 * Second, a tool for classifying a provided job description according to our scheme.
 * Third, a comparison between our classification scheme and existing job titles ability to distinguish between roles.


## Data Understanding
In order to produce our deliverables, we needed a sizable corpus of data industry job descriptions.
We were able to obtain a corpus of 9,485 job descriptions paired with their assigned job titles. 
These job postings were scraped from careerjet.com.

## Data Preparation
Our data preparation process consisted of several steps. 
 1. Converting to lower case and removing new line characters.
 2. Tokenizing text, first by sentence and then by word.
 3. Parts of speech tagging.
 4. Lemmatization.
 5. Removal of stop-words and special characters.
 6. Combining common phrases into $n$-grams for $n=2, 3, 4$.

## Modeling
For this project we produced three models.
 1. An unsupervised topic model, which detects ten distinct topics that are commonly present in data industry job descriptions. This model uses Latent Dirichlet Allocation to infer topics from the provided text. Each job description is represented by a ten dimensional probability vector that describes the proportion of each topic present in the text.
 2. A K-Means clustering of job descriptions based on the topic representation produced by the previous model. This model assigns each job to a class, thereby grouping similar job descriptions together.
 3. A Multinomial Naive Bayes' model, which uses processed job titles to predict the job classification produced by the previous model, without access to the job description. This model seeks to simulate the behavior of a job seeker who skims job titles without reading job descriptions to efficiently reject irrelevant job postings for further review.

## Evaluation
Our key findings from this project are as follows.
 1. Nine out of our ten topics produced by unsupervised learning seem to align well with important data industry skill sets. The remaining topic seems to collect common job posting boiler plate phrases.
 2. Our K-Means clustering of jobs by topic distributions seems to have ten fairly prominent clusters and our selection of a number of clusters is fairly well supported by multiple measures of clustering quality.
 3. Our Naive Bayes' classifier produced 55% classification accuracy. This supports our hypothesis that, in the data industry, job titles are not a particularly accurate predictor of the job description.

## Deployment
We plan to produce a dashboard that will provide an interactive tool for exploring both our topic model and our job classification model.
