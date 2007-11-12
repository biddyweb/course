# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <style>
      .error { color: #990000; }
      img { border: 0px; }
      th {
          border-right: 1px solid #C1DAD7;
          border-bottom: 1px solid #C1DAD7;
          border-top: 1px solid #C1DAD7;
          letter-spacing: 2px;
          text-transform: uppercase;
          text-align: left;
          padding: 6px 6px 6px 12px;
          background: #CAE8EA;
      }
      th.spec {   
          border-left: 1px solid #C1DAD7;
          border-top: 0;
          background: #fff 
          url(${h.url_for('/graphics/bullet1.gif')}) no-repeat;
      }
      th.specalt {
          border-left: 1px solid #C1DAD7;
          border-top: 0;
          background: #f5fafa
          url(${h.url_for('/graphics/bullet2.gif')}) no-repeat;
      }
      td {
          border-right: 1px solid #C1DAD7;
          border-bottom: 1px solid #C1DAD7;
          background: #fff;
          padding: 6px 6px 6px 12px;
      }
  
  
      td.alt {
          background: #F5FAFA;
      }
    </style>
    ${self.head_tags()}
  </head>
  <body>
    ${self.body()}
  </body>
</html>
