# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>Welcome ${session['login_id']}</title>
</%def>

<H1>MOTD</H1>
<blockquote>
<pre>

You are required to come to the recisitation.

#MORE MESSAGES TO BE DROPPED HERE

</pre>
</blockquote>
<H1>END OF MOTD</H1>

${session['login_id']}'s DETAILS
