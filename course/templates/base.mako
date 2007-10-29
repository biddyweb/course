# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <style>
      body { background-color: #fff; color: #333; }
  
      body, p {
        font-family: verdana, arial, helvetica, sans-serif;
        font-size:   12px;
        line-height: 18px;
      }
      pre {
        background-color: #eee;
        padding: 10px;
        font-size: 11px;
        line-height: 13px;
      }
  
      a { color: #000; }
      a:visited { color: #666; }
      a:hover { color: #fff; background-color:#000; }
        
      .error {
          color: #990000;
      }
      th {
          color: #6D929B;
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
          color: #B4AA9D;
      }
      td {
          border-right: 1px solid #C1DAD7;
          border-bottom: 1px solid #C1DAD7;
          background: #fff;
          padding: 6px 6px 6px 12px;
          color: #6D929B;
      }
  
  
      td.alt {
          background: #F5FAFA;
          color: #B4AA9D;
      }
    </style>
    ${self.head_tags()}
  </head>
  <body>
    ${self.body()}
  </body>
</html>
