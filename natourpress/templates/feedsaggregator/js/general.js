$(document).ready(function(){
							$('input[title="SelectBox"]').toggle(function(){
															   $(this).next().css({display:"block"});
															   },function(){
															   $(this).next().css({display:"none"});
															   });
							$('input[title="SelectBox"]').next().hover(function(){}, function(){
								 								$(this).css({display:"none"});
																	  });
							
							$('.SelectHolder .Arrow').toggle(function(){
															   $(this).next().next().css({display:"block"});
															   },function(){
															   $(this).next().next().css({display:"none"});
															   });
							$('#Selector1').find('li').click(function(){
																		$('#Selectbox1').val($(this).attr('title'));
																		$('.Selector').css({display:"none"});
																		});
							$('#Selector2').find('li').click(function(){
																		$('#Selectbox2').val($(this).attr('title'));
																		$('.Selector').css({display:"none"});
																		});
							$('#Selector3').find('li').click(function(){
																		$('#Selectbox3').val($(this).attr('title'));
																		$('.Selector').css({display:"none"});
																		});
							<!--[if lt IE 7]>
							$('li').hover (function () {
								$(this).addClass("hover");
							}, function () {
 								$(this).removeClass("hover");
							});
							$('input[type=button], input[type=submit], input[type=reset]').hover (function () {
  								var CurClass=$(this).attr('class');
								CurClass2=CurClass.split(' ');
								if(CurClass2[0]=="undefined")
									CurClass2[0]=CurClass;
								$(this).addClass(CurClass2[0]+"Hover");
							}, function () {
								var CurClass=$(this).attr('class');
								CurClass2=CurClass.split(' ');
 								$(this).removeClass(CurClass2[1]);
							});
							<!--[endif]-->
						});
