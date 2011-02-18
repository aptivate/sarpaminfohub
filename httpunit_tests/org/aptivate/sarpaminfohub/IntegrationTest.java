package org.aptivate.sarpaminfohub;

import com.meterware.httpunit.WebForm;
import com.meterware.httpunit.WebResponse;

public class IntegrationTest extends SarpamInfoHubTest
{
	private String getSearchPageUrl()
	{
		return "http://localhost:8000";
	}
	
	private WebResponse loadSearchPage() throws Exception
	{
		String searchPageUrl = getSearchPageUrl();
		
		WebResponse response = loadUrl(searchPageUrl);
		
		return response;
	}
	
	public void testSearchForCiprofloxacinReturnsCiprobay() throws Exception
	{
		WebResponse response = loadSearchPage();
		
		WebForm searchForm = response.getFormWithID("search");
		assertNotNull("Unable to find form with ID 'search'", searchForm);
		
		searchForm.setParameter("search", "ciprofloxacin");
		
		response = searchForm.submit();
		
		String resultsPageContent = response.getText();
		
		assertTrue(resultsPageContent.contains("Ciprobay"));
	}
}
