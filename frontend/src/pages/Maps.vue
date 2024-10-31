<template>
  <!-- <div>
    <md-table v-model="users" :md-sort.sync="currentSort" :md-sort-order.sync="currentSortOrder" :md-sort-fn="customSort" md-card>
      <md-table-toolbar>
        <h1 class="md-title">Users</h1>
      </md-table-toolbar>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID" md-numeric>{{ item.id }}</md-table-cell>
        <md-table-cell md-label="Name" md-sort-by="name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Email" md-sort-by="email">{{ item.email }}</md-table-cell>
        <md-table-cell md-label="Gender" md-sort-by="gender">{{ item.gender }}</md-table-cell>
        <md-table-cell md-label="Job Title" md-sort-by="title">{{ item.title }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div> -->

  <div>
    <div id="pdf-content" >
          <p>Tuần thứ: </p>
          <table class="table-bordered" style="width: 863px">
              <tbody>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 62px;">Thứ<br />Ngày/Tháng: </td>
                      <td style="width: 29px; height: 62px;">Tiết</td>
                      <td style="width: 81px; height: 62px;">Môn học</td>
                      <td style="width: 10px; height: 62px;">Tiết theo PPCT</td>
                      <td style="width: 125px; height: 62px;">Tên học sinh nghỉ</td>
                      <td style="width: 173px; height: 62px;">Tên bài, nội dung công việc</td>
                      <td style="width: 226px; height: 62px;">Nhận xét của giáo viên</td>
                      <td style="width: 53px; height: 62px;">Xếp loại tiết học</td>
                      <td style="width: 58px; height: 62px;">Ký tên</td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 310.333px;" rowspan="6">
                          <p>Thứ Hai</p>
                          <p>Ngày:</p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                      </td>
                      <td style="width: 29px; height: 62px;">1</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62.3333px;">
                      <td style="width: 29px; height: 62.3333px;">2</td>
                      <td style="width: 81px; height: 62.3333px;"></td>
                      <td style="width: 10px; height: 62.3333px;"></td>
                      <td style="width: 125px; height: 62.3333px;"></td>
                      <td style="width: 173px; height: 62.3333px;"></td>
                      <td style="width: 226px; height: 62.3333px;"></td>
                      <td style="width: 53px; height: 62.3333px;"></td>
                      <td style="width: 58px; height: 62.3333px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">3</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">4</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">5</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">6</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 62px;" rowspan="6">
                          <p>Thứ Ba</p>
                          <p>Ng&agrave;y:</p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                      </td>
                      <td style="width: 29px; height: 62px;">1</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">2</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">3</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">4</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">5</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">6</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 62px;" rowspan="6">
                          <p>Thứ Tư</p>
                          <p>Ng&agrave;y:</p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                      </td>
                      <td style="width: 29px; height: 62px;">1</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">2</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">3</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">4</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">5</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">6</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 62px;" rowspan="6">
                          <p>Thứ Năm</p>
                          <p>Ng&agrave;y:</p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                      </td>
                      <td style="width: 29px; height: 62px;">1</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">2</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">3</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">4</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">5</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">6</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 62px;" rowspan="6">
                          <p>Thứ S&aacute;u</p>
                          <p>Ng&agrave;y:</p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                      </td>
                      <td style="width: 29px; height: 62px;">1</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">2</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">3</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">4</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">5</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">6</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 62px;" rowspan="6">
                          <p>Thứ Bảy</p>
                          <p>Ng&agrave;y:</p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                      </td>
                      <td style="width: 29px; height: 62px;">1</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">2</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">3</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">4</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">5</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">6</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 82px; height: 62px;" rowspan="6">
                          <p>Chủ Nhật</p>
                          <p>Ng&agrave;y:</p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                          <p></p>
                      </td>
                      <td style="width: 29px; height: 62px;">1</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">2</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">3</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">4</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">5</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
                  <tr style="height: 62px;">
                      <td style="width: 29px; height: 62px;">6</td>
                      <td style="width: 81px; height: 62px;"></td>
                      <td style="width: 10px; height: 62px;"></td>
                      <td style="width: 125px; height: 62px;"></td>
                      <td style="width: 173px; height: 62px;"></td>
                      <td style="width: 226px; height: 62px;"></td>
                      <td style="width: 53px; height: 62px;"></td>
                      <td style="width: 58px; height: 62px;"></td>
                  </tr>
              </tbody>
          </table>
          <div class="row" style="width: 863px">
              <div class="col-md-6">
                  <p>Nhận xét của giáo viên chủ nhiệm lớp:</p>
                  <p>.....................................................................................................................</p>
                  <p>.....................................................................................................................</p>
                  <p>.....................................................................................................................</p>
                  <p>.....................................................................................................................</p>
              </div>
              <div class="col-md-6">
                  <p style="text-align: center;">Giáo viên chủ nhiệm lớp</p>
                  <p style="text-align: center; font-style: italic;">(Ký, ghi rõ họ tên)</p>
              </div>
          </div>
      </div>

      <base-button class="mt-5 mb-5" @click="exportToPdf">Export to pdf</base-button>
  </div>
</template>

<script>
  // export default {
  //   name: 'TableCustomSort',
  //   data: () => ({
  //     currentSort: 'name',
  //     currentSortOrder: 'asc',
  //     users: [
  //       {
  //         id: 1,
  //         name: 'Shawna Dubbin',
  //         email: 'sdubbin0@geocities.com',
  //         gender: 'Male',
  //         title: 'Assistant Media Planner'
  //       },
  //       {
  //         id: 2,
  //         name: 'Odette Demageard',
  //         email: 'odemageard1@spotify.com',
  //         gender: 'Female',
  //         title: 'Account Coordinator'
  //       },
  //       {
  //         id: 3,
  //         name: 'Lonnie Izkovitz',
  //         email: 'lizkovitz3@youtu.be',
  //         gender: 'Female',
  //         title: 'Operator'
  //       },
  //       {
  //         id: 4,
  //         name: 'Thatcher Stave',
  //         email: 'tstave4@reference.com',
  //         gender: 'Male',
  //         title: 'Software Test Engineer III'
  //       },
  //       {
  //         id: 5,
  //         name: 'Clarinda Marieton',
  //         email: 'cmarietonh@theatlantic.com',
  //         gender: 'Female',
  //         title: 'Paralegal'
  //       }
  //     ]
  //   }),
  //   methods: {
  //     customSort (value) {
  //       return value.sort((a, b) => {
  //         const sortBy = this.currentSort

  //         if (this.currentSortOrder === 'desc') {
  //           return a[sortBy].localeCompare(b[sortBy])
  //         }

  //         return b[sortBy].localeCompare(a[sortBy])
  //       })
  //     }
  //   }
  // }
  import html2pdf from 'html2pdf.js';
        
  export default {
    methods: {
      exportToPdf() {
        const element = document.getElementById('pdf-content');
        const options = {
          margin: 1,
          filename: 'lesson_table.pdf',
          html2canvas: { scale: 2, logging: true, dpi: 192, letterRendering: true },
          jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        };
  
        // Generate PDF
        html2pdf().set(options).from(element).save();
      }
    }
  };
</script>