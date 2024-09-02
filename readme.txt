inside EncryptedCookies.py in import _login_ change st.cache to st.cache_data() (Inside functions can be accessed by ctrl+clicking on the function name)
in import _login_ , .utils, Replace the line from trycourier import Courier with from courier.client import Courier.
In authpage.py make sure to provide authtoken which can be generated from https://www.courier.com/email-api/
Remove st.rerun_experimental from __login__
