# -*- coding: utf-8 -*-

<%inherit file="/base.mako" />

<%def name="head_tags()">
    <title>Welcome Teacher</title>
</%def>

<div style="float: right;">
<a href="${h.url_for('math0010', action='logout')}">logout</a>
&nbsp;
<a href="${h.url_for('math0010')}">back to main page</a>
</div>

<h1>Teacher Area</h1>
<br/>

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
    <th scope='col'>${x[0]}</th>
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

