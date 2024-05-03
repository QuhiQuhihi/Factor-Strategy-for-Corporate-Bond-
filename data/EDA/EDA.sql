-- daily_btds table contains daily trade information of corporate bond market
select * from daily_btds limit 10;

-- bond_btds_enhanced table contains tick level trade information of corporate bond market
select * from bond_btds_enhanced limit 10 ;

-- master_corp_agency table shows information of corporate bonds
select * from master_corp_agency limit 10;

-- wrds_fin_ratio table shows id mapping of WRDS, TRACE system.
select * from wrds_mapping 

-- wrds_fin_ratio table shows historical financial ratio info about company (CUSIP, gvkey)
select * from wrds_fin_ratio limit 10;


-- how many bonds included -- realtime db
select count(distinct (substr(cusip_id,0,9))) from bond_btds_enhanced ; -- 333377

-- how many compaby included -- realtime db
select count(distinct (substr(cusip_id,0,8))) from bond_btds_enhanced ; -- 40228

-- how many bonds included -- daily db
select count(distinct (substr(cusip_id,0,9))) from daily_btds  ; -- 167,080

-- how many compaby included -- daily db
select count(distinct (substr(cusip_id,0,8))) from daily_btds ; -- 28,602



-- MSFT bond example (bond cusip : 594918AD6 / MSFT corporate cusip : 594918)

select * from wrds_fin_ratio 
where cusip like '594918%';

select * from master_corp_agency
where cusip_id = '594918AD6';

-- real time data
select * from bond_btds_enhanced 
where cusip_id = '594918AD6';


-- real time data
select trd_exctn_dt ,yld_pt, rptd_pr, entrd_vol_qt 	
from bond_btds_enhanced 
where cusip_id = '594918AD6'
order by trd_exctn_dt desc;

-- daily data
select trans_dt, close_yld , close_pr , close_yld_sign_cd 
from daily_btds  
where cusip_id = '594918AD6'
order by trans_dt desc;

-- daily data with more than 1 month (20 days data point)
select cusip_id, count(*) as aaa
from daily_btds  
group by cusip_id
having aaa > 20;

-- which has more than 20 trading days record : 53,154 notes , 15,506 companies
-- selecting cusip which have longer than 1 month maturity 
select distinct(aa.cusip_id)
from (
	select cusip_id, count(*) as data_point
	from daily_btds  
	group by cusip_id
	having data_point > 20
	order by cusip_id 
) aa;

-- selecting companies which have longer than 1 month maturity 
select distinct(substring(aa.cusip_id,0,8))
from (
	select cusip_id, count(*) as data_point
	from daily_btds  
	group by cusip_id
	having data_point > 20
	order by cusip_id
) aa;





-- daily data with investment return 
select trans_dt, close_pr, close_yld ,
	(close_pr / lag(close_pr,1 ) over (order by trans_dt) - 1.0) as prc_ret,
	(close_yld / lag(close_yld,1 ) over (order by trans_dt) - 1.0) as yld_ret
from daily_btds  
where cusip_id = '594918AD6'
order by trans_dt ;

-- cf chage in prc = chage in yld * delta of duration

-- suspected coupon date for each bond -- return most biggest price loss dates
select trans_dt, (close_pr / lag(close_pr,1 ) over (order by trans_dt) - 1.0) as inv_ret
from daily_btds  
where cusip_id = '594918AD6'
order by inv_ret desc;

-- counting daily data point by cusip id
select bond_sym_id ,count(*) as data_point
from daily_btds 
--WHERE cusip_id is null
group by bond_sym_id 
order by data_point
;



-- historical financial information ratio data of MSFT
select * from wrds_fin_ratio where cusip like '594918%';

-- wrds_fin_ratio table have 3 unique id from each data vendors
select gvkey, cusip , permno  from wrds_fin_ratio;

-- unique id mapping of MSFT bond
select * from wrds_mapping 
where cusip = '594918BV5';

-- check whether TRACE bond price and WRDS fin ratio table have same mapping
select aa.cusip_id, aa.close_pr, bb.cusip
from daily_btds aa
left join 
wrds_fin_ratio bb
on substr(aa.cusip_id,0,8) = bb.cusip;
;

-- check whether TRACE bond price and WRDS fin ratio table have same mapping. Use MSFT bond
select aa.cusip_corp, bb.cusip
from (
	select SUBSTRING(cusip_id,0,7) as cusip_corp
	from daily_btds  
	where cusip_id = '594918BV5'
) aa
left join (
select * from wrds_fin_ratio
where cusip  like '594918%'
) bb
on aa.cusip_corp = bb.cusip
;





