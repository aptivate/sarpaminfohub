package org.aptivate.sarpaminfohub;

import junit.framework.TestCase;

import com.meterware.httpunit.HttpUnitOptions;
import com.meterware.httpunit.WebConversation;
import com.meterware.httpunit.WebResponse;

public class SarpamInfoHubTest extends TestCase 
{
	private WebConversation conversation;
	
	protected void setUp() throws Exception
	{
		conversation = new WebConversation();
        
        HttpUnitOptions.setScriptingEnabled(false);
	}
	
	protected WebResponse loadUrlAndReturnResponse(String url) throws Exception
	{
		WebResponse response = null;
		
		response = conversation.getResponse(url);
		
		return response;
	}
	
	
}
