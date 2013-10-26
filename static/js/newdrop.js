var ma = ["subnav1", "subnav2"];

function dropMenu(x)
{
	for (var m in ma)
	{
		if (ma[m] != x)
		{
			document.getElementById(ma[m]).style.display = "none";
		}
	}

	if (document.getElementById(x).style.display == 'block')
	{
		fadeOut(x);
	}
	else
	{
		fadeIn(x);
	}
}
