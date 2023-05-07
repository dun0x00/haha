-- 特殊用户-薪资统计
SELECT z.xinzi name,count(z.xinzi) value from (
	SELECT case when salary = '面议' then '面议'
					when (y.a+y.b)/2 < 5000 then '小于5千元'
					when (y.a+y.b)/2 >= 5000 && (y.a+y.b)/2 < 10000 then '5千-1万元'
					when (y.a+y.b)/2 >= 10000 && (y.a+y.b)/2 < 15000 then '1万-1.5万元'
					when (y.a+y.b)/2 >= 15000 && (y.a+y.b)/2 < 20000 then '1.5万-2万元'
					when (y.a+y.b)/2 >= 20000 && (y.a+y.b)/2 < 25000 then '2万-2.5万元'
					when (y.a+y.b)/2 >= 25000 && (y.a+y.b)/2 < 3000 then '2万-2.5万元'
					else '大于3万'
					end xinzi
	from (

	SELECT q,
	case when a like '%千'  then a*1000
		 when a like '%千' or a like '%千及以下'  then a*1000
		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000
		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000
		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000
		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0)
		 else 0 end as a,
	case when b like '%千'  then b*1000
		 when b like '%千' or a like '%千及以下'  then b*1000
		 when b like '%万' then b*10000
		 when b like '%万·13薪' or b like '%万·14薪' then b*10000
		 when b like '%万/年' then  round(b*10000/12,0)
		 else 0 end as b,
	salary,search,edu,exp,provinceid,cityid,three_cityid FROM (
		SELECT substring_index( job_salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( job_salary, '-', 1 ) a,SUBSTRING_INDEX( job_salary, '-',- 1 ) b,job_salary salary,search,edu,exp,provinceid,cityid,three_cityid  FROM tbl_job_canji
  where 1=1

	) x

	)y
	) z GROUP BY z.xinzi

-- 特殊用户-薪资预测，计算中位数数据获取
SELECT ( t.a + t.b ) / 2 avg0 FROM (
SELECT q,
	case when a like '%千'  then a*1000
		 when a like '%千' or a like '%千及以下'  then a*1000
		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000
		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000
		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000
		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0)
		 else 0 end as a,
	case when b like '%千'  then b*1000
		 when b like '%千' or a like '%千及以下'  then b*1000
		 when b like '%万' then b*10000
		 when b like '%万·13薪' or b like '%万·14薪' then b*10000
		 when b like '%万/年' then  round(b*10000/12,0)
		 else 0 end as b
	 FROM (
		SELECT substring_index( job_salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( job_salary, '-', 1 ) a,SUBSTRING_INDEX( job_salary, '-',- 1 ) b,job_salary salary,search,edu,exp,provinceid,cityid,three_cityid  FROM tbl_job_canji
  where 1=1

	) x where (x.a != 0 and x.b !=0)

	)t
-- 特殊用户-薪资预测，计算平均数等
SELECT ROUND(avg((a+b)/2),2) avg ,min(t.a) min,max(b) max FROM (
SELECT q,
	case when a like '%千'  then a*1000
		 when a like '%千' or a like '%千及以下'  then a*1000
		 when a not like '%千' and a not like '%万' and b like '%万' then a*10000
		 when a not like '%千' and a not like '%万' and b like '%千' then a*1000
		 when a not like '%千' and a not like '%万' and (b like '%万·13薪' or b like '%万·14薪')then a*10000
		 when a not like '%千' and a not like '%万' and b like '%万/年' then  round(a*10000/12,0)
		 else 0 end as a,
	case when b like '%千'  then b*1000
		 when b like '%千' or a like '%千及以下'  then b*1000
		 when b like '%万' then b*10000
		 when b like '%万·13薪' or b like '%万·14薪' then b*10000
		 when b like '%万/年' then  round(b*10000/12,0)
		 else 0 end as b
	 FROM (
		SELECT substring_index( job_salary, '·13薪', 1 ) AS q,SUBSTRING_INDEX( job_salary, '-', 1 ) a,SUBSTRING_INDEX( job_salary, '-',- 1 ) b,job_salary salary,search,edu,exp,provinceid,cityid,three_cityid  FROM tbl_job_canji
  where 1=1
	) x where (x.a != 0 and x.b !=0)
)t where t.a > 0
