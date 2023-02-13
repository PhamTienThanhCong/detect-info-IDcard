# detect info IDcard (Trích xuất thông tin trong căn cước công dân)
Phân tích và đọc thông tin trong căn cước công dân

## run app 
- Tải đủ model về chạy
  - Model tìm góc chứng minh nhân nhân:
    - link: https://drive.google.com/file/d/1JqzGUrBUVklKUSJP6DHDD7j4hwmY4ZUi/view?usp=share_link
    - Sau đó để tại model/id_card_4_corner.pth
  - Model của viet ORC để nhận diện chữ:
    - Link: https://drive.google.com/uc?id=13327Y1tz1ohsm5YZMyXVMPIOjoOA0OaA
    - Sau đó để tại model/transformerocr.pth
- Chạy code:
  ` Python main.py ` server: http://127.0.0.1:5000
 - demo:
   - Chương trình:
![image](https://user-images.githubusercontent.com/77420469/206903665-6069ff74-57de-4d23-acf9-3b97a8cd2a1f.png)
   - Ảnh test:
![image](https://user-images.githubusercontent.com/77420469/206903706-14040a0d-1f91-4962-8265-baad5f82f38b.png)
   - Kết Quả chạy:
![image](https://user-images.githubusercontent.com/77420469/206903728-aadf3a59-5b86-4cc5-b760-3ca177a6a6f1.png)

- Chúc ae thành công 
