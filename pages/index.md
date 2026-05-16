---
title: 주일예배 부서별 현황
---

```sql sunday_by_dept 
select event_date,  series_group,  total_value from bq.sunday_service 
```
<!-- --> 

```sql series_only
select *
from ${sunday_by_dept}
where series_group is not null
```
<!-- --> 
	
## 주일 부서별 
<BarChart
  data={sunday_by_dept}
  x="event_date"
  y="total_value"
  series=series_group
  title="주일예배 부서별"
  type=grouped
/>

## 주일 부서별 추이 
<LineChart
  data={series_only}
  x="event_date"
  y="total_value"
  series="series_group"
  title="서현 / 송림 / 청년 추이"
  seriesColors={{
    "서현": "#2563eb",
    "송림": "#16a34a",
    "청년": "#f97316"
  }}
/>