--select
--  event_date,
--  series_group,
--  total_value
--from (
  select
    event_date,
    event_date as original_date,
    case
      when department like '%서현%' then '서현'
      when department like '%송림%' then '송림'
      when department like '%청년%' then '청년'
      else '기타'
    end as series_group,
    sum(value) as total_value
  from `bundangwoori-492711.analytics.bq_all`
  where category = '주일예배'
    and event_date is not null
    and department is not null
  group by 
    event_date,
    original_date,
    series_group
  order by event_date asc
--)
--order by
--  original_date asc