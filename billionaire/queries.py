# WITH IndustryNetWorth AS 
# (SELECT 
#         industries,
#         personName,
#         finalWorth,
#         DENSE_RANK() OVER (PARTITION BY industries ORDER BY finalWorth DESC) AS industry_rank
#     FROM 
#         'Billionaires Statistics.csv')
# SELECT 
#     industries, personName, finalWorth, industry_rank
# FROM 
#     IndustryNetWorth
# ORDER BY 
#     industries, industry_rank;

TOP_BY_INDUSTRY_QUERY = """
WITH IndustryNetWorth AS 
(SELECT 
        industries,
        personName,
        finalWorth,
        DENSE_RANK() OVER (PARTITION BY industries ORDER BY finalWorth DESC) AS industry_rank
    FROM 
        df)
SELECT 
    industries, personName, finalWorth, industry_rank
FROM 
    IndustryNetWorth
ORDER BY 
    industries, industry_rank;"""

TOP_BY_INDUSTRY_2_QUERY = """
WITH IndustryNetWorth AS 
(SELECT 
        industries,
        personName,
        finalWorth,
        DENSE_RANK() OVER (PARTITION BY industries ORDER BY finalWorth DESC) AS industry_rank
    FROM 
        df)
SELECT 
    industries, personName, finalWorth, industry_rank
FROM 
    IndustryNetWorth
ORDER BY 
    industries, industry_rank LIMIT 2;"""

DROPDOWN_QUERY = ["SAMPLE", "TOP_BY_INDUSTRY", "TOP_BY_INDUSTRY_2"];

SAMPLE_QUERY = """
SELECT * FROM df;
"""