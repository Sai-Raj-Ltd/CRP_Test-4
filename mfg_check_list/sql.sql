CREATE OR REPLACE FUNCTION public.insert_workorder_check_list_1(
    p_workorder_id integer,
    p_workcenter_id integer)
  RETURNS integer AS
$BODY$
DECLARE

BEGIN
---Inserting Data:-			
insert into mrp_workorder_checklist(op_workorder_id, workcenter_id, checklist_ids)
select p_workorder_id, workcenter_id, id from mrp_checklist 
where workcenter_id = p_workcenter_id
And id not in (select checklist_ids from mrp_workorder_checklist where op_workorder_id = p_workorder_id);

Return 0;
end;       
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

/*
select distinct mw.id as workorder_id, mw.workcenter_id, mc.id as checklist_id from mrp_workorder mw, mrp_checklist mc 
where mw.id = 65 And 
mw.workcenter_id = 3
And mc.workcenter_id = 3
And mc.id not in (select checklist_ids from mrp_workorder_checklist where op_workorder_id = 65);*/


CREATE OR REPLACE FUNCTION public.insert_workorder_check_list_test(
    p_workorder_id integer,
    p_workcenter_id integer)
  RETURNS integer AS
$BODY$
DECLARE

get_order_header_data cursor  for  
select distinct mw.id as workorder_id, mw.workcenter_id, mc.id as checklist_id, mc.description 
from mrp_workorder mw, mrp_checklist mc, mrp_production prd 
where mw.id = p_workorder_id And 
mw.workcenter_id = p_workcenter_id
And mc.workcenter_id = p_workcenter_id
And mc.id not in (select checklist_ids from mrp_workorder_checklist where op_workorder_id = p_workorder_id)
And prd.id=mw.production_id
And prd.routing_id = mc.routing_id;

BEGIN
  FOR header_data in get_order_header_data
	LOOP 
	    BEGIN

			UPDATE mrp_workorder
			SET test_field = (SELECT module_mrp_wo_checklist 
			FROM res_config_settings WHERE id = (SELECT max(id)
			FROM res_config_settings WHERE module_mrp_wo_checklist is not null));


---Inserting Header Data:-			
	INSERT INTO mrp_workorder_checklist
		(
		op_workorder_id, 
		workcenter_id, 
		checklist_ids,
		description
		     ) 
		VALUES
		(
		header_data.workorder_id, 
		header_data.workcenter_id,
		header_data.checklist_id,
		header_data.description
		);
		END;	
	  END loop;		
	Return 0;
end;       
$BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;