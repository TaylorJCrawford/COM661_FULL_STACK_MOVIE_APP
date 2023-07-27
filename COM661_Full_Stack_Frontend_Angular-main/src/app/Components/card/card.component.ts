import { Component, Input, ViewEncapsulation } from '@angular/core';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class CardComponent {
  @Input() id: string = "";
  @Input() title: string = "Error";
  @Input() Overview: string = "Error";
  @Input() movie: any;

  size_cal(text: string){
    console.log(text.substring(0, 350))
    if (text.length > 350) {
      return text.substring(0, 350) + '...'
    }
    return text
  }

  get_star_rating(popularity: number) {
    let result = Math.round(popularity / 5)
    let html = ``
    if(result >= 5) {
      html = `
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span>
        <span class="fa fa-star checked"></span> (`
        + Math.round(popularity * 100) / 100  + ')'
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