# utils/data_export.py

import json
import csv
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
import os

def export_to_json(filename: str, data: Dict[str, List[str]], output_dir: str) -> str:
    """
    Export extracted data to JSON format.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_extracted_{timestamp}.json"
    output_path = os.path.join(output_dir, output_filename)
    
    export_data = {
        "source_file": filename,
        "extraction_timestamp": timestamp,
        "extracted_data": data
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    return output_filename

def export_to_csv(filename: str, data: Dict[str, List[str]], output_dir: str) -> str:
    """
    Export extracted data to CSV format.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_extracted_{timestamp}.csv"
    output_path = os.path.join(output_dir, output_filename)
    
    # Flatten the data for CSV
    rows = []
    for key, values in data.items():
        for value in values:
            rows.append({
                "source_file": filename,
                "category": key,
                "value": value,
                "timestamp": timestamp
            })
    
    # Write to CSV
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        if rows:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
    
    return output_filename

def export_to_excel(filename: str, data: Dict[str, List[str]], output_dir: str) -> str:
    """
    Export extracted data to Excel format with multiple sheets.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_extracted_{timestamp}.xlsx"
    output_path = os.path.join(output_dir, output_filename)
    
    with pd.ExcelWriter(output_path) as writer:
        # Summary sheet
        summary_data = {
            'Category': [],
            'Count': [],
            'Values': []
        }
        
        for key, values in data.items():
            summary_data['Category'].append(key)
            summary_data['Count'].append(len(values))
            summary_data['Values'].append(', '.join(values[:3]) + ('...' if len(values) > 3 else ''))
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Detailed sheets for each category
        for key, values in data.items():
            if values:
                df = pd.DataFrame({key: values})
                sheet_name = key[:31]  # Excel sheet names have max 31 chars
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return output_filename

def export_batch_results(results: List[Dict[str, Any]], output_dir: str) -> str:
    """
    Export batch processing results to a comprehensive report.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"batch_extraction_{timestamp}.json"
    output_path = os.path.join(output_dir, output_filename)
    
    # Prepare summary statistics
    total_files = len(results)
    successful = sum(1 for r in results if r['status'] == 'success')
    failed = sum(1 for r in results if r['status'].startswith('error'))
    no_text = sum(1 for r in results if r['status'] == 'no_text_detected')
    
    export_data = {
        "batch_timestamp": timestamp,
        "summary": {
            "total_files": total_files,
            "successful": successful,
            "failed": failed,
            "no_text_detected": no_text
        },
        "results": results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    # Also create a CSV summary
    csv_filename = f"batch_summary_{timestamp}.csv"
    csv_path = os.path.join(output_dir, csv_filename)
    
    csv_rows = []
    for result in results:
        row = {
            "filename": result['filename'],
            "status": result['status']
        }
        
        if result['status'] == 'success' and result['product_info']:
            info = result['product_info']
            row.update({
                "product_names": ', '.join(info.get('product_names', [])),
                "retailer_names": ', '.join(info.get('retailer_names', [])),
                "prices": ', '.join(info.get('prices', [])),
                "dates": ', '.join(info.get('dates', []))
            })
        
        csv_rows.append(row)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        if csv_rows:
            writer = csv.DictWriter(f, fieldnames=csv_rows[0].keys())
            writer.writeheader()
            writer.writerows(csv_rows)
    
    return output_filename

def export_to_text(filename: str, data: Dict[str, List[str]], output_dir: str) -> str:
    """
    Export extracted data to a formatted text file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(filename)[0]
    output_filename = f"{base_name}_extracted_{timestamp}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"Product Information Extraction Report\n")
        f.write(f"Source File: {filename}\n")
        f.write(f"Extraction Date: {timestamp}\n")
        f.write("=" * 50 + "\n\n")
        
        for category, values in data.items():
            f.write(f"{category.upper()}:\n")
            if values:
                for value in values:
                    f.write(f"  - {value}\n")
            else:
                f.write("  - Not Detected\n")
            f.write("\n")
    
    return output_filename