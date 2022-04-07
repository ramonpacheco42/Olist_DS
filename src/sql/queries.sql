SELECT dt_sgmt, COUNT( DISTINCT seller_id ) 
FROM tb_seller_sgmt
GROUP BY dt_sgmt
