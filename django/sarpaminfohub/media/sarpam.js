function openLinkedInWindow(url)
{
    var windowName = '';
    window.open(url,
        windowName, 'width=600,height=402');
    return false;
}

function openLinkedInWindowWithCheck(url)
{
    if (window.confirm("Are you sure you wish to delete your profile?"))
    {
        return openLinkedInWindow(url);    
    }
    else
    {
        return false;
    }
}