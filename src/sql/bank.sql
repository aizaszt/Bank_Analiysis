---Топ банков по прибыли
SELECT bank, SUM(net_profit) AS total_profit
FROM bank_db
GROUP BY bank
ORDER BY total_profit DESC
LIMIT 5;

--Эффективность (доходы vs расходы)
SELECT 
    bank,
    SUM("%income") AS income,
    SUM("%expence") AS expense,
    SUM("%income") - SUM("%expence") AS profit_margin
FROM bank_db
GROUP BY bank
ORDER BY profit_margin DESC
LIMIT 5;

--Надёжность (активы + капитал)
SELECT 
    bank,
    AVG(assets) AS avg_assets,
    AVG(capital) AS avg_capital
FROM bank_db
GROUP BY bank
ORDER BY avg_assets DESC
LIMIT 5;

--Популярность (депозиты)
SELECT 
    bank,
    SUM(deposit) AS total_deposits
FROM bank_db
GROUP BY bank
ORDER BY total_deposits DESC
LIMIT 5;

--Удобный app 
SELECT 
    bank,
    rank
FROM app
ORDER BY rank DESC
LIMIT 5;


-- сколько прибыли получает за доходы
SELECT 
    bank,
    ROUND(SUM(net_profit) * 100.0 / SUM("%income"), 2) AS profit_margin_percent
FROM bank_db
GROUP BY bank
ORDER BY profit_margin_percent DESC
LIMIT 5;

--Насколько эффективно банк использует свои ресурсы
SELECT 
    bank,
    ROUND(SUM(net_profit) * 100.0 / SUM(assets), 2) AS roa_percent
FROM bank_db
GROUP BY bank
ORDER BY roa_percent DESC
LIMIT 5;

--эффективность для инвесторов
SELECT 
    bank,
    ROUND(SUM(net_profit) * 100.0 / SUM(capital), 2) AS roe_percent
FROM bank_db
GROUP BY bank
ORDER BY roe_percent DESC
LIMIT 5;

--Сколько банк тратит от доходов
SELECT 
    bank,
    ROUND(SUM("%expence") * 100.0 / SUM("%income"), 2) AS expense_ratio
FROM bank_db
GROUP BY bank
ORDER BY expense_ratio ASC
LIMIT 5;


--сколько комиссии берет с клиента
SELECT 
    bank,
    ROUND(SUM(com_income) * 100.0 / SUM("%income"), 2) AS commission_share
FROM bank_db
GROUP BY bank
ORDER BY commission_share DESC
LIMIT 5;

--Насколько банк зависит от клиентов
SELECT 
    bank,
    ROUND(SUM(deposit) * 100.0 / SUM(assets), 2) AS deposit_ratio
FROM bank_db
GROUP BY bank
ORDER BY deposit_ratio DESC
LIMIT 5;

-- Процент неработающих кредитов (NPL) к общему портфелю
-- Ищем банки с самым чистым портфелем (ASC - от меньшего к большему)
SELECT 
    bank,
    year,
    ROUND(("NPL" * 100.0 / NULLIF(loan, 0))::numeric, 2) AS npl_ratio_percent
FROM bank_db
WHERE year = 2025
ORDER BY npl_ratio_percent ASC
LIMIT 5;

-- Доля валютного дохода в общей прибыли
SELECT 
    bank,
    ROUND(("FX income" * 100.0 / NULLIF(net_profit, 0))::numeric, 2) AS fx_dependency_percent
FROM bank_db
WHERE year = 2025 AND net_profit > 0
ORDER BY fx_dependency_percent DESC;

-- Сравнение адекватности капитала текущего года с предыдущим
SELECT 
    bank,
    year,
    "capital_adequacy" AS current_k21,
    LAG("capital_adequacy") OVER (PARTITION BY bank ORDER BY year) AS prev_k21,
    "capital_adequacy" - LAG("capital_adequacy") OVER (PARTITION BY bank ORDER BY year) AS k21_change
FROM bank_db
WHERE year IN (2024, 2025)
ORDER BY k21_change ASC; 

