package org.aptivate.sarpaminfohub;

import org.aptivate.web.utils.HtmlIterator;

import com.meterware.httpunit.WebForm;
import com.meterware.httpunit.WebResponse;

public class IntegrationTest extends SarpamInfoHubTest
{
	private static String host = "http://localhost:8000/";
	
	private String getSearchPageUrl()
	{
		return host;
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
	
	public void testSuppliersPageValidates() throws Exception
	{
		WebResponse response = loadSearchPage("formulation_suppliers/1/test");
		validatePage(response);
	}
	
	public void testContactSearchPageValidates() throws Exception
	{
		WebResponse response = loadContactSearchPage("");
		validatePage(response);
	}
	
	public void testContactTagsPageValidates() throws Exception
	{
		WebResponse response = loadContactSearchPage("tags/Bioethics/");
		validatePage(response);
	}
	
	public void testContactPageValidates() throws Exception
	{
		WebResponse response = loadContactSearchPage("2/");
		validatePage(response);
	}
	
	public void testContactSearchResultsValidates() throws Exception
	{
		WebResponse response = loadContactSearchPage("");
		WebForm searchForm = response.getForms()[0];
		
		searchForm.setParameter("search_term", "Bell");
		
		response = searchForm.submit();
		validatePage(response);
	}
	
	public void testContactSearchWithNoResultsValidates() throws Exception
	{
		WebResponse response = loadContactSearchPage("");
		WebForm searchForm = response.getForms()[0];
		
		searchForm.setParameter("search_term", "Flooble");
		
		response = searchForm.submit();
		validatePage(response);
	}
	
	private WebResponse loadContactSearchPage(String path) throws Exception
	{
		String url = getContactSearchPageUrl(path);
		
		WebResponse response = loadUrl(url);
		
		return response;
	}
	
	private String getContactSearchPageUrl(String path)
	{
		return host + "contacts/" + path; 
	}
}
