# Appsmith Configuration

1. Drag a **FilePicker** widget onto the canvas and enable multiple file upload.
2. Set the **onFilesSelected** action to call the `/process` API with the
   selected files.
3. Display the returned `job_id` and poll `/results/{{job_id}}` to enable the
   download button once the API responds with the Excel workbook.
4. Use a **Button** widget to fetch `/results/{{job_id}}` and trigger the file
   download when available.
