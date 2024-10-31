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
    
    <!-- Bang hien thi -->
    <div ref="tableRef">
      <p>Tuần thứ: </p>
            <table class="table-bordered" style="width: 863px">
                <tbody>
                    <tr style="height: 62px;">
                        <td style="width: 82px; height: 62px;">dab<br />Ngày/Tháng: </td>
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

    <base-button class="mt-5 mb-5" @click="generatePDF()">Export to pdf</base-button>
  </div>
</template>

<script>
import { ref, nextTick } from "vue";
import jsPDF from "jspdf";
import domtoimage from "dom-to-image";

export default {
  setup() {
    const tableRef = ref(null);

    const generatePDF = () => {
      nextTick(() => {
        const table = tableRef.value;
        if (!table) return; // Đảm bảo bảng tồn tại

        // Kích thước A4
        const pdfWidth = 595;  // Chiều rộng A4
        const pdfHeight = 842; // Chiều cao A4

        // Chuyển đổi bảng HTML sang hình ảnh PNG bằng dom-to-image
        domtoimage.toPng(table).then((imageData) => {
          // Tạo tài liệu jsPDF mới
          const pdf = new jsPDF("l", "pt", [pdfWidth, pdfHeight]);

          // Thêm hình ảnh PNG vào tài liệu PDF
          pdf.addImage(imageData, "PNG", 0, 0, pdfWidth, pdfHeight);

          // Kiểm tra nếu tài liệu lớn hơn kích thước A4
          const pageHeight = pdf.internal.pageSize.height;
          const imgHeight = pdf.getImageProperties(imageData).height * (pdfWidth / pdf.getImageProperties(imageData).width);
          let heightLeft = imgHeight;

          let position = 0;

          // Nếu hình ảnh quá cao, chia thành nhiều trang
          while (heightLeft >= 0) {
            position = heightLeft - imgHeight;
            pdf.addPage();
            pdf.addImage(imageData, "PNG", 0, position, pdfWidth, imgHeight);
            heightLeft -= pageHeight;
          }

          // Lưu tài liệu PDF
          pdf.save("table.pdf");
        });
      });
    };

    return {
      tableRef,
      generatePDF,
    };
  },
};
</script>