SELECT t1.*,
		CASE WHEN pct_receita <= 0.5 and pct_freq <= 0.5 then 'BAIXO V. BAIXO F.'
		WHEN pct_receita > 0.5 and pct_freq <= 0.5 then 'ALTO VALOR'
		WHEN pct_receita <= 0.5 and pct_freq > 0.5 then 'ALTA FREQ'
		WHEN pct_receita < 0.9 or pct_freq < 0.9 then 'PRODUTIVO'
		ELSE 'SUPER PRODUTIVO'
		END AS segmento_valor_freq,

		CASE WHEN qtde_dias_base <= 60 THEN 'INICIO'
			WHEN qtde_dias_base >= 300 THEN 'RETENCAO'
			ELSE 'ATIVO'
		END AS segmento_vida,

		'{date_end}' AS dt_sgmt

FROM (		
	SELECT t1.*,
		percent_rank() over (order by receita_total asc) as pct_receita,
		percent_rank() over (order by qtde_pedidos  asc) as pct_freq
	FROM (
		SELECT t2.seller_id,
			round(sum(t2.price),2) as receita_total,
			count(DISTINCT(t1.order_id)) as qtde_pedidos,
			count(t2.product_id) AS qtde_produtos,
			count(distinct(t2.product_id)) as qtade_destinta,
			min(DATEDIFF( '{date_end}', t1.order_approved_at)) as qtde_dias_ult_venda,
			max(datediff('{date_end}', dt_inicio)) as qtde_dias_base
		FROM olist.tb_orders as t1
		LEFT JOIN olist.tb_order_items as t2 ON t1.order_id = t2.order_id
		LEFT JOIN (
			select t2.seller_id, 
				min(date( t1.order_approved_at)) as dt_inicio
			from tb_orders as t1
			left join tb_order_items as t2 on t1.order_id = t2.order_id
			group by t2.seller_id 
		) as t3 on t2.seller_id = t3.seller_id  
		WHERE t1.order_approved_at BETWEEN '{date_init}' and '{date_end}'
		group by t2.seller_id
	) as t1
) AS T1
WHERE seller_id IS NOT NULL