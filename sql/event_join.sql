select

from
    public.srpinpid pd,
	public.srsites sites,
    public.srevents evt,
    public.srevpart evrev
where
	pd.siteid = sites.siteid and
	sites.eventid = evt.eventid and
	evrev.