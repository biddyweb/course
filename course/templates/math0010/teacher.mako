# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>
    Welcome
    ${c.teacher_info['given_names']}
    ${c.teacher_info['surname']}
    </title>
    <style>
        nobr { white-space: nowrap; }
        .smalltext {font-size: small;} 
        .centertext {text-align: center;} 
        blockquote pre{font-size: x-large; background: #CAE8EA;}
    </style>
</%def>


<h1>Teacher Area</h1>
<br/>
% if c.message:
<blockquote>
<pre>
${c.message}
</pre>
</blockquote>
% endif
<div>
  <h3> Students' Details </h3>
<table>
  <tr>
    <th scope='col'>ID</th>
    <th scope='col'>Name</th>
    <th scope='col'>Email</th>
##    <th scope='col'>Program</th>
##    <th scope='col'>Major</th>
% for x in c.all_marks[0][1:]:
    <th scope='col' class='centertext'><nobr>${x[0]}</nobr><br/>
    <nobr class='smalltext'>${x[2]}</nobr></th>
% endfor
  </tr>
<%
class_th = ['spec', 'specalt']
class_td = ['', 'alt']
%>
% for x in range(len(c.all_marks)):
  <tr>
    <td class="${class_td[x % len(class_td)]}">${c.all_marks[x][0].id}</td>
    <td class="${class_td[x % len(class_td)]}">${c.all_marks[x][0].surname}
    ,&nbsp; ${c.all_marks[x][0].given_names}</td>
    <td class="${class_td[x % len(class_td)]}" style="text-align: center;">
    <% email = c.all_marks[x][0].email %>
    % if email:
      <a href="mailto:${email}">
        <img src="${h.url_for('/graphics/email.png')}" alt='Email' />
      </a>
    % else:
        <img src="${h.url_for('/graphics/not_available.png')}" alt='N/A' />
    % endif
    </td>
##    <td class="${class_td[x % len(class_td)]}"> ${c.all_marks[x][0].program}</td>
##    <td class="${class_td[x % len(class_td)]}">${c.all_marks[x][0].major}</td>
% for y in c.all_marks[x][1:]:
    % if type(y[1]) == float:
        <td class="${class_td[x % len(class_td)]}">${'%6.2f%%'%y[1]}</td>
    % else:
        <td class="${class_td[x % len(class_td)]}">${'%6s'%y[1]}</td>
    % endif
% endfor
  </tr>
% endfor
</table>
</div>

<h3>Downloads</h3>
    <span> <a href="${h.url_for('/downloads/%s'%x)}">${c.files[0]}</a> </span>
% for x in c.files[1:]:
    ,&nbsp;<span> <a href="${h.url_for('/downloads/%s'%x)}">${x}</a> </span>
% endfor


</div>
<br/>
<br/>
<a href="${h.url_for('math0010')}">back to main page</a>
&nbsp;
<a href="${h.url_for('math0010', action='logout')}">logout</a>
