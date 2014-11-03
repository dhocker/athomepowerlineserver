import urllib2
import re
import io
import datetime

#
# TODO Rework this to be able to look up a given date.
# The downside is that it requires an Internet connection.
#

# Sunrise/sunset tabled cache
sun_table_cache = {}
def _get_sun_table(year_to_get):
  """
  Return the sunrise/sunset table for a given year
  """
  if year_to_get not in sun_table_cache:
    # Get the sunrise/sunset table from the navy site for Buford, GA. Change as needed.
    url = 'http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl?FFX=1&xxy={0}&type=0&st=GA&place=Buford&ZZZ=END'.format(year_to_get)
    response = urllib2.urlopen(url)
    sun_table_cache[year_to_get] = response.read()
    
  return sun_table_cache[year_to_get]

def get_sun_data_for_date(year_or_date, month=None, day=None):
  """
  Return the sunrise/sunset time for a given date.
  year_or_date = Either a datetime.date type or a year (20nn)
  month = 1-12
  day = 1-31
  """
  if isinstance(year_or_date, datetime.date):
    year = year_or_date.year
    month = year_or_date.month
    day = year_or_date.day
  else:
    year = year_or_date
    
  # Get the table for the given year
  html = _get_sun_table(year)

  # Find the line that contains the specified day
  pattern = '^{0:02}(.*)$'.format(day)
  m = re.search(pattern, html, re.MULTILINE)
  line = m.group(0)

  # Extract the day from the line
  x = 4 + (11 * (month - 1))
  sunrise = "{0}:{1}".format(line[x:x+2], line[x+2:x+4])
  sunset = "{0}:{1}".format(line[x+5:x+5+2], line[x+5+2:x+5+4])
  if (not sunrise.startswith(" ")):
    return (sunrise, sunset)
  # Invalid date (day isn't in month)
  return None

def generate_sunrise_sunset_sql(year_to_get, table_name):
  """
  Generates SQL insert statements for sunset/sunrise in a given year.
  """
  # Get the sunrise/sunset table from the navy site for Buford, GA. Change as needed.
  html = _get_sun_table(year_to_get)

  filename = "sunrise_sunset_{0}.sql".format(year_to_get)
  fh = open(filename, 'w')

  # find the year
  pattern = 'Rise and Set for the Sun for (\d+)'
  m = re.search(pattern, html)
  year = int(m.group(1))
  print "Year:", year

  # Prototypical insert statement
  sql_template = "insert into {0} values (\"{1}\",time(\"{2}\"),time(\"{3}\"));\n"

  # Go through the table by day (each row in the table is a day of the month)
  for day in range(1, 32):
    # Beginning of line starts with two-digit day
    pattern = '^{0:02}(.*)$'.format(day)
    m = re.search(pattern, html, re.MULTILINE)
    line = m.group(0)
    
    # This is all positional. And, there are blank values
    # where months do not have days (e.g. Feb 31).
    x = 4
    for m in range(1, 13):
      sunrise = "{0}:{1}".format(line[x:x+2], line[x+2:x+4])
      sunset = "{0}:{1}".format(line[x+5:x+5+2], line[x+5+2:x+5+4])
      if (not sunrise.startswith(" ")):
        sundate = datetime.date(year, m, day)
        sql = sql_template.format(table_name, str(sundate), sunrise, sunset)
        fh.write(sql)
      x += 11
    
  fh.close()
  
if __name__ == "__main__":
  # generate_sunrise_sunset_sql(2014, "sun_table")
  # generate_sunrise_sunset_sql(2015, "sun_table")
  # generate_sunrise_sunset_sql(2016, "sun_table")
  
  # for y in range(2017, 2024):
    # print y
    # generate_sunrise_sunset_sql(y, "sun_table")
  
  print get_sun_data_for_date(2014, 2, 17)
  print get_sun_data_for_date(2014, 2, 29)
  print get_sun_data_for_date(2014, 2, 18)
  print get_sun_data_for_date(2014, 2, 19)
  print "2014-02-20:", get_sun_data_for_date(datetime.date(2014, 2, 20))
  
#
# Here's the source for a page
#
"""  
 <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>Sun or Moon Rise/Set Table for One Year</title>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
</head>
<body>
<pre>
             o  ,    o  ,                                   BUFORD, GEORGIA                            Astronomical Applications Dept.
Location: W084 00, N34 07                          Rise and Set for the Sun for 2016                   U. S. Naval Observatory        
                                                                                                       Washington, DC  20392-5420     
                                                         Eastern Standard Time                                                        
                                                                                                                                      
                                                                                                                                      
       Jan.       Feb.       Mar.       Apr.       May        June       July       Aug.       Sept.      Oct.       Nov.       Dec.  
Day Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set  Rise  Set
     h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m   h m  h m
01  0742 1737  0734 1806  0704 1833  0623 1857  0546 1920  0525 1943  0528 1952  0548 1937  0610 1901  0631 1819  0656 1743  0724 1726
02  0742 1738  0733 1807  0703 1834  0621 1858  0545 1921  0525 1943  0529 1951  0548 1936  0611 1900  0632 1818  0657 1742  0725 1726
03  0742 1739  0732 1808  0702 1834  0620 1859  0544 1922  0525 1944  0529 1951  0549 1935  0611 1858  0632 1817  0658 1741  0726 1726
04  0742 1740  0731 1809  0700 1835  0619 1900  0543 1923  0525 1944  0530 1951  0550 1934  0612 1857  0633 1815  0659 1740  0726 1726
05  0742 1740  0730 1810  0659 1836  0617 1900  0542 1924  0524 1945  0530 1951  0551 1933  0613 1856  0634 1814  0700 1739  0727 1726
06  0742 1741  0730 1811  0658 1837  0616 1901  0541 1924  0524 1946  0531 1951  0551 1932  0613 1854  0635 1813  0701 1738  0728 1726
07  0742 1742  0729 1812  0656 1838  0615 1902  0540 1925  0524 1946  0531 1951  0552 1931  0614 1853  0635 1811  0702 1737  0729 1726
08  0742 1743  0728 1813  0655 1839  0613 1903  0540 1926  0524 1946  0532 1950  0553 1930  0615 1852  0636 1810  0703 1737  0730 1727
09  0742 1744  0727 1814  0654 1839  0612 1903  0539 1927  0524 1947  0532 1950  0553 1929  0615 1850  0637 1809  0704 1736  0730 1727
10  0742 1745  0726 1815  0653 1840  0611 1904  0538 1927  0524 1947  0533 1950  0554 1928  0616 1849  0638 1807  0705 1735  0731 1727
11  0742 1746  0725 1816  0651 1841  0609 1905  0537 1928  0524 1948  0533 1949  0555 1927  0617 1847  0638 1806  0705 1734  0732 1727
12  0742 1747  0724 1817  0650 1842  0608 1906  0536 1929  0524 1948  0534 1949  0556 1926  0617 1846  0639 1805  0706 1734  0733 1727
13  0742 1747  0723 1818  0649 1843  0607 1906  0535 1930  0524 1949  0535 1949  0556 1925  0618 1845  0640 1804  0707 1733  0733 1728
14  0742 1748  0722 1818  0647 1843  0606 1907  0535 1930  0524 1949  0535 1948  0557 1923  0619 1843  0641 1802  0708 1732  0734 1728
15  0742 1749  0721 1819  0646 1844  0604 1908  0534 1931  0524 1949  0536 1948  0558 1922  0620 1842  0642 1801  0709 1732  0735 1728
16  0741 1750  0720 1820  0644 1845  0603 1909  0533 1932  0524 1950  0537 1947  0559 1921  0620 1840  0642 1800  0710 1731  0735 1729
17  0741 1751  0719 1821  0643 1846  0602 1909  0533 1933  0524 1950  0537 1947  0559 1920  0621 1839  0643 1759  0711 1731  0736 1729
18  0741 1752  0718 1822  0642 1847  0601 1910  0532 1933  0524 1950  0538 1946  0600 1919  0622 1838  0644 1758  0712 1730  0736 1729
19  0740 1753  0717 1823  0640 1847  0559 1911  0531 1934  0525 1950  0539 1946  0601 1918  0622 1836  0645 1756  0713 1730  0737 1730
20  0740 1754  0716 1824  0639 1848  0558 1912  0531 1935  0525 1951  0539 1945  0601 1916  0623 1835  0646 1755  0714 1729  0738 1730
21  0740 1755  0715 1825  0638 1849  0557 1913  0530 1936  0525 1951  0540 1945  0602 1915  0624 1833  0647 1754  0715 1729  0738 1731
22  0739 1756  0714 1826  0636 1850  0556 1913  0530 1936  0525 1951  0541 1944  0603 1914  0624 1832  0647 1753  0716 1729  0739 1731
23  0739 1757  0713 1827  0635 1850  0555 1914  0529 1937  0525 1951  0541 1943  0604 1913  0625 1831  0648 1752  0717 1728  0739 1732
24  0738 1758  0711 1828  0634 1851  0554 1915  0528 1938  0526 1951  0542 1943  0604 1912  0626 1829  0649 1751  0718 1728  0739 1732
25  0738 1759  0710 1828  0632 1852  0553 1916  0528 1938  0526 1951  0543 1942  0605 1910  0627 1828  0650 1750  0719 1728  0740 1733
26  0737 1800  0709 1829  0631 1853  0551 1916  0528 1939  0526 1952  0543 1941  0606 1909  0627 1826  0651 1749  0719 1727  0740 1734
27  0737 1801  0708 1830  0629 1853  0550 1917  0527 1940  0527 1952  0544 1941  0606 1908  0628 1825  0652 1748  0720 1727  0741 1734
28  0736 1802  0707 1831  0628 1854  0549 1918  0527 1940  0527 1952  0545 1940  0607 1906  0629 1824  0653 1746  0721 1727  0741 1735
29  0736 1803  0705 1832  0627 1855  0548 1919  0526 1941  0527 1952  0545 1939  0608 1905  0629 1822  0653 1745  0722 1727  0741 1736
30  0735 1804             0625 1856  0547 1920  0526 1942  0528 1952  0546 1938  0608 1904  0630 1821  0654 1744  0723 1727  0741 1736
31  0734 1805             0624 1856             0526 1942             0547 1937  0609 1902             0655 1744             0742 1737

                                             Add one hour for daylight time, if and when in use.

</pre>
<p><a href="javascript:history.go(-1)">Back to form</a></p>
</body>
</html>
"""