var _scrollbar_width;
var _tvno = [];
var _movieno = [];

jQuery(function($){
$(document).ready(function() {
	// スクロールバーの幅を取得
	var _scrollbartest = $('<div>').css({
		width: '100px',
		height: '100px',
		overflow: 'scroll',
		position: 'absolute',
		top: '-9999px'
	});
	_scrollbartest.appendTo('body');
	_scrollbar_width = _scrollbartest.get(0).offsetWidth - _scrollbartest.get(0).clientWidth;
	//console.log(_scrollbar_width);
	_scrollbartest.remove();
});
});


function _modal_popup_message() {
	$('.modalBK').show(0,function(){
		$('.modalBody').show(0,function(){
			var _modal_html_height = $(this).find('.modalhtml').height();
			var _modal_margin_top = -( (_modal_html_height+50) / 2 +10 );
			$(this)
				.height(_modal_html_height)
				.css('marginTop',_modal_margin_top);
			$('body').css({
				position: 'relative',
				overflow: 'hidden',
				paddingRight: _scrollbar_width+'px'
			});
		});
	});
}
function _modal_popup_thanks() {
	$('.modalBK').show(0,function(){
		$('.modalBodyThanks').show(0,function(){
			var _modal_html_height = $(this).find('.modalhtml').height();
			var _modal_margin_top = -( (_modal_html_height+50) / 2 +10 );
//			$(this)
//				.height(_modal_html_height)
//				.css('marginTop',_modal_margin_top);
			_modal_body = $(this);
			_modal_width = _modal_body.width();
			_modal_height = _modal_body.height();
			_modal_left_position = Number(_modal_width)/2 +20;
			_modal_left_position = '-' + String(_modal_left_position) + 'px';
			_modal_top_position = Number(_modal_height)/2 +20;
			_modal_top_position = '-' + String(_modal_top_position) + 'px';
			_modal_body.css({
				marginLeft: _modal_left_position,
				marginTop: _modal_top_position
			});
			$('body').css({
				position: 'relative',
				overflow: 'hidden',
				paddingRight: _scrollbar_width+'px'
			});
		});
	});
}
function _modal_popup_message_close() {
	$('.modalBK').fadeOut(200);
	$('.modalBody, .modalBodyThanks').hide();
	$('body').css({
		position: 'static',
		overflow: 'auto',
		paddingRight: '0px'
	});
}


// 選択機能2018 初期化
var _checked = new Object();
_checked.tv = new Object();
_checked.tv.count = 3;
_checked.tv.result = [];
_checked.movie = new Object();
_checked.movie.count = 3;
_checked.movie.result = [];
_checked.all = 0;



jQuery(function($){
$(document).ready(function() {

// サンクスメッセージ
var _has_thanks = $('#modalBodyThanksShow').length;
//console.log(_has_thanks);
if(_has_thanks) {
	_modal_popup_thanks();
}



//チェックボックスをクリックするとイベント発火
/*
$("input[type=checkbox]").click(function(){
    var $count = $("input[type=checkbox]:checked").length;
    var $not = $('input[type=checkbox]').not(':checked')

        //チェックが3つ付いたら、チェックされてないチェックボックスにdisabledを加える
    if($count >= 3) {
        $not.attr("disabled",true);
    }else{
        //3つ以下ならisabledを外す
        $not.attr("disabled",false);
    }
});
*/


// モーダルウィンドウ
$('.bt_vote').on('click',function(e){
	e.preventDefault();
	
	// リンクの data-vote-title をモーダル中の文言にセット
	//var _vote_title = $(this).attr('data-vote-title');
	//$('#confirm-vote-title, #confirm-vote-title-twitter').text(_vote_title);
	
	_checked.tv.confirm = $('#vote-tv-confirm');
	_checked.movie.confirm = $('#vote-movie-confirm');
	_checked.tv.confirm.empty();
	_checked.movie.confirm.empty();
	
	// TV部門
	if ( _checked.tv.result.length > 0 ) { // 0以上の場合にリスト出力
		$('.confirm-vote-tv').show();
		$.each(_checked.tv.result, function(i,val){
			_checked.tv.confirm.append('<li>'+val+'</li>');
                        _i = i + 1;
                        $("#post-tv-id"+_i).val(_tvno[i]);
		});
	} else { // 0件の場合は一覧非表示
		$('.confirm-vote-tv').hide();
	}
	// 劇場映画部門
	if ( _checked.movie.result.length > 0 ) { // 0以上の場合にリスト出力
		$('.confirm-vote-movie').show();
		$.each(_checked.movie.result, function(i,val){
			_checked.movie.confirm.append('<li>'+val+'</li>');
                        _i = i + 1;
                        $("#post-movie-id"+_i).val(_movieno[i]);
		});
	} else { // 0件の場合は一覧非表示
		$('.confirm-vote-movie').hide();
	}
	
	// Twitter投稿プレビュー用テキスト処理
	_checked.tv.preview = [];
	_checked.movie.preview = [];
	$.each(_checked.tv.result, function(i,val){
		if ( val.length > 17 ) {
			val = val.substr(0,17) + '…';
		}
		_checked.tv.preview.push(val);
	});
	$.each(_checked.movie.result, function(i,val){
		if ( val.length > 17 ) {
			val = val.substr(0,17) + '…';
		}
		_checked.movie.preview.push(val);
	});
	$('#confirm-vote-tv-twitter').text( _checked.tv.preview.join('／') );
	$('#confirm-vote-movie-twitter').text( _checked.tv.preview.join('／') );
	
	//a add 作品No 2014.11.29
	// var _vote_post_id = $(this).attr('data-vote-id');
	//$('#confirm-vote-post-id').val(_vote_post_id);

	// モーダルウィンドウを表示
	$('.modalBK').show(0,function(){
		$('.modalBody').show(0,function(){
			var _window_height = window.innerHeight ? window.innerHeight: $(window).height();
			var _modal_height = _window_height -120;
			var _modal_window_margin_top = -( (_modal_height) / 2 +20 );
			_modal_body = $(this);
			_modal_width = _modal_body.width();
			_modal_height = _modal_body.height();
			_modal_left_position = Number(_modal_width)/2;
			_modal_left_position = '-' + String(_modal_left_position) + 'px';
			_modal_top_position = Number(_modal_height)/2;
			_modal_top_position = '-' + String(_modal_top_position) + 'px';
			_window_height = window.innerHeight;
			if ( _window_height < _modal_height ) {
				_modal_body.css({
					marginLeft: _modal_left_position,
					marginTop: '-' + (_window_height/2-10) + 'px',
					height: (_window_height-20) + 'px'
				});
			} else {
				_modal_body.css({
					marginLeft: _modal_left_position,
					marginTop: _modal_top_position
				});
			}
			var _scroll = $(window).scrollTop();
			$('body').css({
				position: 'relative',
				overflow: 'hidden',
				paddingRight: _scrollbar_width+'px'
			});
		});
	});
});
$('.close').on('click',function(e){
	e.preventDefault();
	$('.modalBody').hide(0,function(){
		$('.modalBK').fadeOut(200);
	});
	$('body').css({
		position: 'static',
		overflow: 'auto',
		paddingRight: '0px'
	});
});


});
});



// 選択機能2018
function _check() {
	
	// 集計前の初期化
	_checked.tv.count = 3;
	_checked.tv.result = [];
	_checked.movie.count = 3;
	_checked.movie.result = [];

        _tvno = [];
        _movieno = [];
	
	// 選択色/非活性色を一旦全てクリア
	$('.vote-list > li').removeClass('votecheck-checked disabled');
	// チェック済要素各々の状態を取得して保存
	var _checkbox = $('input[type="checkbox"]:checked');
	_checkbox.each(function(){
		var _li = $(this).closest('li');
		_li.addClass('votecheck-checked');
		if ( _li.hasClass('tv') ) {
			--_checked.tv.count;
			_checked.tv.result.push( $(this).val() );
			_tvno.push( $(this).attr('id') );
		} else {
			--_checked.movie.count;
			_checked.movie.result.push( $(this).val() );
			_movieno.push( $(this).attr('id') );
		}
	});
	
	// チェック合計数
	_checked.all = _checkbox.length;
	// 総計が1以上の場合に投票ボタンを表示
	if ( _checked.all < 1 ) {
		$('#vote-submit').prop('disabled',true);
	} else {
		$('#vote-submit').prop('disabled',false);
	}
	
	// カテゴリごとの合計数を出力
	$('#vote-clipboard-tv .vote-count-num').text(_checked.tv.count);
	$('#vote-clipboard-movie .vote-count-num').text(_checked.movie.count);
	
	// 結果ラベルをリスト出力
	_checked.tv.list = $('#vote-clipboard-tv .vote-clipboard-list');
	_checked.movie.list = $('#vote-clipboard-movie .vote-clipboard-list');
	_checked.tv.list.empty();
	_checked.movie.list.empty();
	$.each(_checked.tv.result, function(i,val){
		_checked.tv.list.append('<li>'+val+'</li>');
	});
	$.each(_checked.movie.result, function(i,val){
		_checked.movie.list.append('<li>'+val+'</li>');
	});
	
	// 規定数で入力を止める
	var _tv_list_not_checked = $('li.tv input[type="checkbox"]:not(:checked)');
	var _movie_list_not_checked = $('li.movie input[type="checkbox"]:not(:checked)');
	if ( _checked.tv.count == 0 ) {
		_tv_list_not_checked.prop('disabled',true).closest('li').addClass('disabled');
	} else {
		_tv_list_not_checked.prop('disabled',false);
	}
	if ( _checked.movie.count == 0 ) {
		_movie_list_not_checked.prop('disabled',true).closest('li').addClass('disabled');
	} else {
		_movie_list_not_checked.prop('disabled',false);
	}
	
	// 3件ずつ選択肢終わった場合は、選択済み一覧を表示する
	if ( _checked.tv.count == 0 && _checked.movie.count == 0 ) {
		$('.vote-clipboard-list').addClass('list-show');
	}
	
	
	//console.log(_checked);
}

jQuery(function($){
$(function(){1
	
	// チェック要素確認
	_check();
	$('input[type="checkbox"]').on('change',function(event){
		_check();
	});
	
	// 画面幅768px以下 選択済み一覧の表示制御
	if ( window.matchMedia('(max-width:768px)').matches ) {
		$('#vote-clipboard h3').on('click',function(){
			var _ul = $(this).parent().find('ul');
			if ( _ul.hasClass('list-show') ) {
				$(this).parent().find('ul').removeClass('list-show');
			} else {
				$(this).parent().find('ul').addClass('list-show');
			}
		});
	}
	
});
});


