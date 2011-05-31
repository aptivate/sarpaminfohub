package org.aptivate.sarpaminfohub;

import java.math.BigInteger;

import org.aptivate.web.utils.HtmlIterator;

import com.meterware.httpunit.WebForm;
import com.meterware.httpunit.WebResponse;
import com.meterware.httpunit.controls.SelectionFormControl;

public class IntegrationTest extends SarpamInfoHubTest
{
	private static String host = "http://localhost:8000/";
	
	public void testSearchForCiprofloxacinReturnsCiprofloxacin500mg() throws Exception
	{
		WebResponse response = loadPageAndReturnResponse("/search/");
		
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
		WebResponse response = loadPageAndReturnResponse("/search/");
		validatePage(response);
	}
	
	public void testSearchPageWithResultsValidates() throws Exception
	{
		WebResponse response = loadPageAndReturnResponse("/search/?search=ciprofloxacin");
		validatePage(response);
	}
	
	public void testFormulationPageValidates() throws Exception
	{
		WebResponse response = loadPageAndReturnResponse("formulation/1/");
		validatePage(response);
	}
	
	public void testSuppliersPageValidates() throws Exception
	{
		WebResponse response = loadPageAndReturnResponse("formulation_suppliers/1/test");
		validatePage(response);
	}
	
	public void testContactSearchPageValidates() throws Exception
	{
		WebResponse response = loadContactSearchPage("");
		validatePage(response);
	}
	
	public void testContactTagsPageValidates() throws Exception
	{
		String hexEncodedTag = toHex("procurement");
		
		WebResponse response = loadContactSearchPage("tags/" + hexEncodedTag);
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
		
		WebResponse response = loadUrlAndReturnResponse(url);
		
		return response;
	}
	
	private String getContactSearchPageUrl(String path)
	{
		return host + "contacts/" + path; 
	}
	
	public void testFormulationProductPageValidates() throws Exception
	{
		WebResponse response = loadPageAndReturnResponse("formulation_products/1");
		
		validatePage(response);
	}

	public void testSupplierPageValidates() throws Exception
	{
		WebResponse response = loadPageAndReturnResponse("suppliers/1");
		
		validatePage(response);
	}
	
	public void testProductPageValidates() throws Exception
	{
		WebResponse response = loadPageAndReturnResponse("product/1");
		
		validatePage(response);
	}
	
	public void testSearchByTagReturnsMatch() throws Exception
	{
		WebResponse response = loadContactSearchPage("");
		
		WebForm searchForm = response.getForms()[0];
		                            
		SelectionFormControl tagSelect = (SelectionFormControl)searchForm.getControlWithID("input_4");
		
		String [] optionValues = tagSelect.getOptionValues();
		String [] displayedOptions = tagSelect.getDisplayedOptions();
		
		int i;
		
		for (i = 0; i < optionValues.length; i++)
		{
			if (displayedOptions[i].equals("capacity building"))
				break;
		}
		
		assertTrue(i < optionValues.length);
		
		String [] selectedValues = {optionValues[i]};
		
		searchForm.setParameter("tags", selectedValues);
		
		response = searchForm.submit();
		
		String resultsPageContent = response.getText();
		
		assertTrue(resultsPageContent.contains("Rose Shija"));
	}
	
	private WebResponse loadPageAndReturnResponse(String relativeUrl) throws Exception
	{
		WebResponse response = loadUrlAndReturnResponse(host + relativeUrl);
		
		return response;
	}
	
	public String toHex(String arg) {
	    return String.format("%x", new BigInteger(arg.getBytes()));
	}

}
