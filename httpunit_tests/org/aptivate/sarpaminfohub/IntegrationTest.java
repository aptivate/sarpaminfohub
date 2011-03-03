package org.aptivate.sarpaminfohub;

import org.aptivate.web.utils.HtmlIterator;

import com.meterware.httpunit.WebForm;
import com.meterware.httpunit.WebResponse;

public class IntegrationTest extends SarpamInfoHubTest
{
	private String getSearchPageUrl()
	{
		return "http://localhost:8000/";
	}
	
	private WebResponse loadSearchPage(String query) throws Exception
	{
		String searchPageUrl = getSearchPageUrl();
		
		WebResponse response = loadUrl(searchPageUrl + query);
		
		return response;
	}	
	
	private WebResponse loadSearchPage() throws Exception
	{
		return loadSearchPage("");
	}
	
	public void testSearchForCiprofloxacinReturnsCiprofloxacin500mg() throws Exception
	{
		WebResponse response = loadSearchPage();
		
		WebForm searchForm = response.getFormWithID("search");
		assertNotNull("Unable to find form with ID 'search'", searchForm);
		
		searchForm.setParameter("search", "ciprofloxacin");
		
		response = searchForm.submit();
		
		String resultsPageContent = response.getText();
		
		assertTrue(resultsPageContent.contains("ciprofloxacin 500mg tablet"));
	}
	
	private void validatePage(WebResponse response) throws Exception
	{
		new HtmlIterator(response.getText());
	}
	
	public void testSearchPageValidates() throws Exception
	{
		WebResponse response = loadSearchPage();
		validatePage(response);
	}
	
	public void testSearchPageWithResultsValidates() throws Exception
	{
		WebResponse response = loadSearchPage("?search=ciprofloxacin");
		validatePage(response);
	}
	
	public void testFormulationPageValidates() throws Exception
	{
		WebResponse response = loadSearchPage("formulation/1/");
		validatePage(response);
	}
}
