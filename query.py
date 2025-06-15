import streamlit as st

class MobilisationQueries:
    def __init__(self, report_name):
        self.report_name = report_name

    def give_query(self):
        if self.report_name == "PC Selection Summary Report":
            query =	""" 
                with pc_cert_record_attempt as (
                select pct.pc_id,
                pct.test_grade,
                pct.created_at,
                ROW_NUMBER() over (partition by pct.pc_id order by created_at asc) as attempt_number
                from pms_pragati_rpt_pc_training pct
                )
                select
                UPPER(pcs.working_state) as "State Name",
                pmt.pc_target as "Target",
                CONCAT(round(COUNT(distinct pcs.pc_id) *100 / pmt.pc_target), '%') as "% PC Onboarded",
                SUM(case when pcra.test_grade = 'Master' then 1 else 0 end) as "Total Master Level",
                SUM(case when pcra.test_grade = 'Expert' then 1 else 0 end) as "Total Expert Level",
                SUM(case when pcra.test_grade = 'Beginner' then 1 else 0 end) as "Total Begineer Level"
                from (select * from pms_pragati_rpt_pc_selected pcss 
                where pcss.cohort_year = '2025-26' 
                and pcss.pc_status  = 'Selected' 
                and pcss.ip_name != 'MW IP' and (pcss.working_state is not null and pcss.working_state not in (''))) as pcs
                left join pc_cert_record_attempt pcra
                on pcra.pc_id = pcs.pc_id and pcra.attempt_number = 1
                left join (select distinct pmts.state_name, sum(pmts.pc_target) as pc_target from pragati_2025_mobilization_target pmts
                group by pmts.state_name) pmt
                on UPPER(pmt.state_name) = pcs.working_state
                group by UPPER(pcs.working_state),pmt.pc_target          
            """
            return query

        elif self.report_name == 'Village Selection Summary Report':
            query = """ 
                with
                visited_village as (select UPPER(pvp.state) as state,
                coalesce(count(distinct pvp.village_ward_code), 0) as total_visited_village 
                from (select * from pms_pragati_rpt_priority_village_profile pvps
                where pvps.cohort_year = '2025-26' and pvps.ip_name != 'MW IP' and pvps.status = 'Saved') as pvp
                group by UPPER(pvp.state)),
                shortlisted_village as (
                select UPPER(pvp.state) as state,
                coalesce(count(distinct pvp.village_ward_code), 0) as total_submitted_village
                from (select * from pms_pragati_rpt_priority_village_profile pvps
                where pvps.cohort_year = '2025-26' and pvps.ip_name != 'MW IP' and pvps.status = 'Submitted') as pvp
                group by UPPER(pvp.state)
                ),
                approved_village as (
                select UPPER(pvp.state) as state,
                coalesce(count(distinct pvp.village_ward_code), 0) as total_approved_village
                from (select * from pms_pragati_rpt_priority_village_profile pvps
                where pvps.cohort_year = '2025-26' and pvps.ip_name != 'MW IP' and pvps.status = 'Approved') as pvp
                group by UPPER(pvp.state)
                )
                select 
                UPPER(vv.state) AS "State Name", 
                pmt.village_target as "Target",
                CONCAT(ROUND(vv.total_visited_village*100 / pmt.village_target), '%') as "% Visted",
                CONCAT(coalesce(ROUND(sv.total_submitted_village*100 / pmt.village_target), 0), '%') as "% Shortlisted",
                concat(coalesce(round(av.total_approved_village*100 / pmt.village_target), 0), '%') as "% Approved"
                from visited_village vv
                left join shortlisted_village sv
                on UPPER(sv.state) = UPPER(vv.state)
                left join approved_village av
                on UPPER(av.state) = UPPER(av.state)
                left join (select distinct pmts.state_name, sum(pmts.prerak_target) as village_target from pragati_2025_mobilization_target pmts
                group by pmts.state_name) as pmt
                on UPPER(pmt.state_name) = UPPER(vv.state)
            """
            return query            
        else:
            st.warning("Oops !! Required Report Query Is Not Available")
            return ""
           
