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

BILLIONAIRE_QUERY = """
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

SAMPLE_QUERY = """
SELECT * FROM df;
"""