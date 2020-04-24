import json
import csv

#Specify the columns that you exported and are inputing to the script, i.e.:
my_columns = ['base_customer_charge','callback_metadata','callback_status_code','callback_url','created_on','csv_upload_id','day','download_url','error','extra_moderator_statuses','file_id','finished_on','flags','focus','frame_url','image_url','known_status','label_data','media_deleted','hash_media','media_height','media_width','medias','original_filename','project_id','status','status_to_edit','tags','hash_task','task_id','task_units','text_data','timestamp','total_customer_charge']

#Specify the input path for the exported results
in_path = 'exported.csv' 

#Specify the output paath where the processsed results should be written to
out_path = 'processed.csv'

with open(in_path, 'r') as infile:
    reader = csv.DictReader(infile, delimiter=',', quotechar='"')
    
    with open(out_path, 'w') as outfile:

        writer = csv.writer(outfile, delimiter=',')
        my_columns.remove('status') if 'status' in my_columns else None
        writer.writerow(my_columns + ['logo','left','top','right','bottom'])
        
        for row in reader:  

            # Preserve all exported data except the status
            out_row = []
            for col in my_columns:
                if col == 'status': continue 
                out_row.append(row[col])
            
            # Extract the logo detections from the 'status' response json
            if row['status']: #Check for non-empty status
                # Parse json to obtain the bounding boxes
                bboxes = json.loads(row['status'])[0]['response']['output'][0]['bounding_poly']
                
                # Extract the logo information from each bounding box
                for box in bboxes: 
                    logo = box['classes'][0]['class']
                    left = box['dimensions']['left']
                    top  = box['dimensions']['top']
                    right = box['dimensions']['right']
                    bottom = box['dimensions']['bottom']
                    
                    writer.writerow(out_row + [logo, left, top, right, bottom])