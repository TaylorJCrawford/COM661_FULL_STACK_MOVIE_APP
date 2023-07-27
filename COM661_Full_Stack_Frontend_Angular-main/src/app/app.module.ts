import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AgGridModule  } from 'ag-grid-angular';
import {NgxPaginationModule} from 'ngx-pagination';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';
import {FormsModule} from '@angular/forms';

import { AppComponent } from './app.component';
import { NavBarComponent } from './Components/nav-bar/nav-bar.component';
import { HomeComponent } from './Components/home/home.component';
import { FeedComponent } from './Components/feed/feed.component';
import { CardComponent } from './Components/card/card.component';
import { MovieComponent } from './Components/movie/movie.component';
import { ReviewCardComponent } from './Components/review-card/review-card.component';
import { Top10Component } from './Components/top10/top10.component';
import { WebService } from './Components/Services/web.service';
import { MovieFormComponent } from './Components/movie-form/movie-form.component';
import { EditCommentFormComponent } from './Components/edit-comment-form/edit-comment-form.component';
import { CharacterCardsComponent } from './Components/character-cards/character-cards.component';
import { WatchlistComponent } from './Components/watchlist/watchlist.component';
import { AdminPanelComponent } from './Components/admin-panel/admin-panel.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

var routes: any = [
  {
    // Home
    path: '',
    component: HomeComponent
  },
  {
    // Top 10
    path: 'top10',
    component: Top10Component
  },
  {
    // Feed
    path: 'feed',
    component: FeedComponent
  },
  {
    // View Movie
    path: 'movie/:title',
    component: MovieComponent
  },
  {
    path: 'movie/edit/:title/:comment_id',
    component: EditCommentFormComponent
  },
  {
    // Search Term
    path: 'movie/search/:search_term',
    component: FeedComponent
  },
  {
    // Edit Movie
    path: 'movie/edit/:title',
    component: MovieFormComponent
  },
  {
    // Add New Movie
    path: 'movie/new/add',
    component: MovieFormComponent
  },
  {
    // View Watchlist for user.
    path: 'watchlist/:user_id',
    component: WatchlistComponent
  },
  {
    path: 'admin',
    component: AdminPanelComponent
  }
];
@NgModule({
  declarations: [
    AppComponent,
    NavBarComponent,
    HomeComponent,
    FeedComponent,
    CardComponent,
    MovieComponent,
    ReviewCardComponent,
    Top10Component,
    MovieFormComponent,
    EditCommentFormComponent,
    CharacterCardsComponent,
    WatchlistComponent,
    AdminPanelComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    NgxPaginationModule,
    ReactiveFormsModule,
    AgGridModule,
    BrowserAnimationsModule
  ],
  providers: [WebService],
  bootstrap: [AppComponent]
})
export class AppModule { }