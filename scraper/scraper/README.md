Cách chạy Project
- Thông tin chung (đăng nhập facebook)
    - login_type:
        - 0: tài khoản mật khẩu
        - 1: cookie
- Fanpage: cần những thông tin sau
    - url fanpage ở trang mbasic
    - max_scroll_timeline: số lần cuộn trang
    - max scroll_comment: số lần cuộn comment

- Ví dụ: 
    - scrapy crawl facebook-fanpage -a username=email -a password=password -a login_type=0 -a fanpage_url='https://mbasic.facebook.com/langthanghanoiofficial' -a max_scroll_timeline=5 -a max_scroll_comment=5

    - scrapy crawl facebook-fanpage -a cookie='copy-file-cookie' -a login_type=1 -a fanpage_url='https://mbasic.facebook.com/langthanghanoiofficial' -a max_scroll_timeline=5 -a max_scroll_comment=5