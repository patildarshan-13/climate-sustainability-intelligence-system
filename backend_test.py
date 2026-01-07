import requests
import sys
import json
import time
from datetime import datetime
from pathlib import Path

class EcoIntelAPITester:
    def __init__(self, base_url="https://esg-intel.preview.emergentagent.com"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.tests_run = 0
        self.tests_passed = 0
        self.test_results = []

    def log_test(self, name, success, details=""):
        """Log test result"""
        self.tests_run += 1
        if success:
            self.tests_passed += 1
        
        result = {
            "test_name": name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status} - {name}")
        if details:
            print(f"   Details: {details}")

    def test_api_root(self):
        """Test API root endpoint"""
        try:
            response = requests.get(f"{self.api_url}/", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Message: {data.get('message', 'No message')}"
            self.log_test("API Root Endpoint", success, details)
            return success
        except Exception as e:
            self.log_test("API Root Endpoint", False, f"Error: {str(e)}")
            return False

    def test_stats_endpoint(self):
        """Test stats endpoint"""
        try:
            response = requests.get(f"{self.api_url}/stats", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Stats: {data}"
            self.log_test("Stats Endpoint", success, details)
            return success, response.json() if success else {}
        except Exception as e:
            self.log_test("Stats Endpoint", False, f"Error: {str(e)}")
            return False, {}

    def test_get_documents(self):
        """Test get documents endpoint"""
        try:
            response = requests.get(f"{self.api_url}/documents", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            if success:
                data = response.json()
                details += f", Document count: {len(data)}"
            self.log_test("Get Documents", success, details)
            return success, response.json() if success else []
        except Exception as e:
            self.log_test("Get Documents", False, f"Error: {str(e)}")
            return False, []

    def test_document_upload(self):
        """Test document upload with a sample text file"""
        try:
            # Create a sample text file
            sample_content = """Climate Change Report 2024
            
This is a sample sustainability report for testing purposes.
It contains information about carbon emissions, renewable energy initiatives, and environmental impact assessments.

Key findings:
- Carbon emissions reduced by 15% compared to previous year
- Renewable energy adoption increased to 45% of total energy consumption
- Water usage efficiency improved by 20%
- Waste reduction programs achieved 30% decrease in landfill waste

Recommendations:
- Continue investment in renewable energy infrastructure
- Implement more aggressive carbon reduction targets
- Expand circular economy initiatives
- Enhance biodiversity conservation programs
"""
            
            # Create temporary file
            temp_file = Path("/tmp/test_climate_report.txt")
            temp_file.write_text(sample_content)
            
            # Upload file
            with open(temp_file, 'rb') as f:
                files = {'file': ('test_climate_report.txt', f, 'text/plain')}
                response = requests.post(f"{self.api_url}/documents/upload", files=files, timeout=30)
            
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Document ID: {data.get('id')}, Status: {data.get('status')}"
                # Clean up
                temp_file.unlink()
                self.log_test("Document Upload", success, details)
                return success, data
            else:
                details += f", Error: {response.text}"
                self.log_test("Document Upload", success, details)
                return False, {}
                
        except Exception as e:
            self.log_test("Document Upload", False, f"Error: {str(e)}")
            return False, {}

    def test_query_without_documents(self):
        """Test query when no documents are available"""
        try:
            query_data = {
                "question": "What are the main climate risks?",
                "top_k": 5
            }
            response = requests.post(f"{self.api_url}/query", json=query_data, timeout=15)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Answer: {data.get('answer', '')[:100]}..."
            
            self.log_test("Query Without Documents", success, details)
            return success, response.json() if success else {}
        except Exception as e:
            self.log_test("Query Without Documents", False, f"Error: {str(e)}")
            return False, {}

    def test_query_with_documents(self, document_id=None):
        """Test query after uploading documents"""
        try:
            # Wait a bit for document processing
            time.sleep(3)
            
            query_data = {
                "question": "What are the key findings about carbon emissions?",
                "top_k": 5
            }
            response = requests.post(f"{self.api_url}/query", json=query_data, timeout=20)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                answer = data.get('answer', '')
                sources = data.get('sources', [])
                details += f", Answer length: {len(answer)}, Sources: {len(sources)}"
                
                # Check if answer contains relevant information
                if "carbon" in answer.lower() or "emission" in answer.lower():
                    details += " (Relevant answer found)"
                else:
                    details += " (Answer may not be relevant)"
            
            self.log_test("Query With Documents", success, details)
            return success, response.json() if success else {}
        except Exception as e:
            self.log_test("Query With Documents", False, f"Error: {str(e)}")
            return False, {}

    def test_delete_document(self, document_id):
        """Test document deletion"""
        if not document_id:
            self.log_test("Delete Document", False, "No document ID provided")
            return False
            
        try:
            response = requests.delete(f"{self.api_url}/documents/{document_id}", timeout=10)
            success = response.status_code == 200
            details = f"Status: {response.status_code}"
            
            if success:
                data = response.json()
                details += f", Message: {data.get('message', '')}"
            
            self.log_test("Delete Document", success, details)
            return success
        except Exception as e:
            self.log_test("Delete Document", False, f"Error: {str(e)}")
            return False

    def run_all_tests(self):
        """Run all backend tests"""
        print("🚀 Starting EcoIntel Backend API Tests")
        print(f"Testing against: {self.api_url}")
        print("=" * 60)
        
        # Test basic endpoints
        api_working = self.test_api_root()
        if not api_working:
            print("❌ API is not responding. Stopping tests.")
            return self.get_summary()
        
        # Test stats and documents
        stats_working, stats_data = self.test_stats_endpoint()
        docs_working, docs_data = self.test_get_documents()
        
        # Test query without documents
        self.test_query_without_documents()
        
        # Test document upload
        upload_success, upload_data = self.test_document_upload()
        document_id = upload_data.get('id') if upload_success else None
        
        # Test query with documents (if upload was successful)
        if upload_success:
            self.test_query_with_documents(document_id)
            
            # Test document deletion
            if document_id:
                self.test_delete_document(document_id)
        
        return self.get_summary()

    def get_summary(self):
        """Get test summary"""
        success_rate = (self.tests_passed / self.tests_run * 100) if self.tests_run > 0 else 0
        
        summary = {
            "total_tests": self.tests_run,
            "passed_tests": self.tests_passed,
            "failed_tests": self.tests_run - self.tests_passed,
            "success_rate": f"{success_rate:.1f}%",
            "test_results": self.test_results
        }
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print(f"Total Tests: {self.tests_run}")
        print(f"Passed: {self.tests_passed}")
        print(f"Failed: {self.tests_run - self.tests_passed}")
        print(f"Success Rate: {success_rate:.1f}%")
        
        return summary

def main():
    tester = EcoIntelAPITester()
    summary = tester.run_all_tests()
    
    # Save results to file
    results_file = Path("/app/backend_test_results.json")
    with open(results_file, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📁 Results saved to: {results_file}")
    
    # Return appropriate exit code
    return 0 if summary["failed_tests"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())