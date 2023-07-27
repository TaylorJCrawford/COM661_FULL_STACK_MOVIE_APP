import { Component, ViewEncapsulation } from '@angular/core';
import { WebService } from '../Services/web.service';

@Component({
  selector: 'app-top10',
  templateUrl: './top10.component.html',
  styleUrls: ['./top10.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class Top10Component {

  top_movies_list: any = [];

  html3Stars = `
  <span class="fa fa-star checked"></span>
  <span class="fa fa-star checked"></span>
  <span class="fa fa-star checked"></span>
  <span class="fa fa-star "></span>
  <span class="fa fa-star "></span>`

  constructor(public webService: WebService) { }

  ngOnInit() {
    this.top_movies_list = this.webService.get_top_10();
  }

  getrank(i: number) {

    let value = ''

    if (i == 0) {
      i = i + 1
      value = i.toString() + '<sup class="rank1">st</sup>'
    } else if (i == 1) {
      i = i + 1
      value = i.toString() + '<sup class="rank2">nd</sup>'
    } else if (i == 2) {
      i = i + 1
      value = i.toString() + '<sup class="rank3">rd</sup>'
    } else {
      i = i + 1
      value = i.toString() + '<sup>th</sup>'
    }

    return value
  }

  get_rank_value(rank: number) {

    let html = ``

    if (rank == 0) {
      html = `
          <h1 class="rank_1" style="color: #FFCE30;">1<sup>st</sup></h1>
      `
    } else if (rank == 1) {
      html = `
          <h1 class="rank" style="color: #288BA8;">2<sup>nd</sup></h1>
      `
    } else if (rank == 2) {
      html = `
          <h1 class="rank" style="color: #5534eb;">3<sup>rd</sup></h1>
        `
    } else {
      html = "<h1 class='rank'>" + (rank + 1).toString() + "<sup>th</sup></h1>"
    }

    return html
  }

  get_star_rating(popularity: number) {
    let result = Math.round(popularity / 5)
    let html = ``
    if (result >= 5) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span> (`
        + Math.round(popularity * 100) / 100 + ')'
    } else if (result == 4) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span> (`
        + Math.round(popularity * 100) / 100 + ')'
    } else if (result == 3) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span> (`
        + Math.round(popularity * 100) / 100 + ')'
    } else if (result == 2) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span> (`
        + Math.round(popularity * 100) / 100 + ')'
    } else if (result == 1) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span> (`
        + Math.round(popularity * 100) / 100 + ')'
    } else {
      html = `
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span>
        <span class="fa fa-star"></span> (`
        + Math.round(popularity * 100) / 100 + ')'
    }

    return html
  }
}
