<template>
  <div class="row">
     <div class="row ml-2">
      <div class="">
        <h3 class="font-weight-bold">Kết quả học tập</h3>
      </div>
      <!-- <div class="col-md-6">
        <div
              class="btn-group btn-group-toggle float-right"
              data-toggle="buttons"
            >
              <label
                v-for="(option, index) in adminstrationOption"
                :key="option"
                class="btn btn-sm btn-primary btn-simple"
                :class="{ active: bigLineChart.activeIndex === index }"
                :id="index"
              >
                <input
                  type="radio"
                  @click="initBigChart(index)"
                  name="options"
                  autocomplete="off"
                  :checked="bigLineChart.activeIndex === index"
                />
                {{ option }}
              </label>
            </div>
      </div> -->
    </div>
          
    <div class="col-md-12" v-if="bigLineChart.activeIndex === 0">
      <score-detail></score-detail>
    </div>
    <div class="col-md-12" v-if="bigLineChart.activeIndex === 1">
      <!-- <score-statistic></score-statistic> -->
    </div>
    <div class="col-md-12" v-if="bigLineChart.activeIndex === 2">
      
    </div>
  </div>
</template>

<script>

import config from "@/config";
import ScoreDetail from './LearningOutcome/ScoreDetail.vue';
import ScoreStatistic from './LearningOutcome/ScoreStatistic.vue';


export default {
  components: { 
    ScoreDetail,
    ScoreStatistic
  },
  computed: {
    adminstrationOption() {
      return this.$t("dashboard.learningOutcome");
    },
  },
  data() {
    return {
      bigLineChart: {
        activeIndex: 0,
        index: "Quản trị",
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: [],
      },
    }
  },
  methods: {
    initBigChart(index) {
      let chartData = {
        datasets: [
          {
            fill: true,
            borderColor: config.colors.primary,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: config.colors.primary,
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: config.colors.primary,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
          },
        ],
        labels: [
          "JAN",
          "FEB",
          "MAR",
          "APR",
          "MAY",
          "JUN",
          "JUL",
          "AUG",
          "SEP",
          "OCT",
          "NOV",
          "DEC",
        ],
      };

      this.bigLineChart.chartData = chartData;
      this.bigLineChart.activeIndex = index;
    },
  }

}
</script>

<style>

</style>