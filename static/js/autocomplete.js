/**
 A jQuery plugin for search hints

 Author: Lorenzo Cioni - https://github.com/lorecioni
 */

(function ($) {
    $.fn.autocomplete = function (params) {

        //Selections
        var currentSelection = -1;
        var currentProposals = [];

        //Default parameters
        params = $.extend({
            id: "input",
            hints: [],
            placeholder: '请输入导师姓名或者专业进行搜索',
            width: 500,
            height: 40,
            showButton: true,
            buttonText: 'Search',
            onSubmit: function (text) {
            },
            onBlur: function () {
            }
        }, params);

        //Build messagess
        this.each(function () {
            //Container
            // position: absolute;
            var searchContainer = $('<div></div>')
                .attr("style", "position: absolute;\n" +
                    "    top: 30%;\n" +
                    "    left: 50%;\n" +
                    "    transform: translate( -50%,-50%);\n" +
                    "    height: 42px;\n" +
                    "    border-radius: 30px;\n" +
                    "    padding: 10px;")
                .css('height', params.height * 2);

            //Text input
            var input = $('<input type="text" autocomplete="off" name="query">')
                .attr('placeholder', params.placeholder)
                .attr('id', params.id)
                .attr("style", " width:400px;\n" +
                    "            height: 40px;\n" +
                    "            border:1px solid green;\n" +
                    "            /*清除掉默认的padding*/\n" +
                    "            padding:0px;\n" +
                    "\n" +
                    "            /*提示字首行缩进*/\n" +
                    "            text-indent: 10px;\n" +
                    "\n" +
                    "            /*去掉蓝色高亮框*/\n" +
                    "            outline: none;\n" +
                    "\n" +
                    "            /*用浮动解决内联元素错位及小间距的问题*/\n" +
                    "            float:left;")
                .css({
                    'width': "400px",
                    'height': "40px"
                });

            if (params.showButton) {
                input.css('border-radius', '3px 0 0 3px');
            }

            //Proposals
            var proposals = $('<div></div>')
                .addClass('proposal-box')
                .css('width', params.width + 18)
                .css('top', input.height() + 20);
            var proposalList = $('<ul></ul>')
                .addClass('proposal-list');

            proposals.append(proposalList);

            input.keydown(function (e) {
                switch (e.which) {
                    case 38: // Up arrow
                        e.preventDefault();
                        $('ul.proposal-list li').removeClass('selected');
                        if ((currentSelection - 1) >= 0) {
                            currentSelection--;
                            $("ul.proposal-list li:eq(" + currentSelection + ")")
                                .addClass('selected');
                        } else {
                            currentSelection = -1;
                        }
                        break;
                    case 40: // Down arrow
                        e.preventDefault();
                        if ((currentSelection + 1) < currentProposals.length) {
                            $('ul.proposal-list li').removeClass('selected');
                            currentSelection++;
                            $("ul.proposal-list li:eq(" + currentSelection + ")")
                                .addClass('selected');
                        }
                        break;
                    case 13: // Enter
                        if (currentSelection > -1) {
                            var text = $("ul.proposal-list li:eq(" + currentSelection + ")").html();
                            input.val(text);
                        }
                        currentSelection = -1;
                        proposalList.empty();
                        params.onSubmit(input.val());
                        break;
                    case 27: // Esc button
                        currentSelection = -1;
                        proposalList.empty();
                        input.val('');
                        break;
                }
            });

            input.bind("change paste keyup", function (e) {
                if (e.which != 13 && e.which != 27
                    && e.which != 38 && e.which != 40) {
                    currentProposals = [];
                    currentSelection = -1;
                    proposalList.empty();
                    if (input.val() != '') {
                        var word = "^" + input.val() + ".*";
                        proposalList.empty();
                        for (var test in params.hints) {
                            if (params.hints[test].match(word)) {
                                currentProposals.push(params.hints[test]);
                                var element = $('<li></li>')
                                    .html(params.hints[test])
                                    .addClass('proposal')
                                    .click(function () {
                                        input.val($(this).html());
                                        proposalList.empty();
                                        params.onSubmit(input.val());
                                    })
                                    .mouseenter(function () {
                                        $(this).addClass('selected');
                                    })
                                    .mouseleave(function () {
                                        $(this).removeClass('selected');
                                    });
                                proposalList.append(element);
                            }
                        }
                    }
                }
            });

            input.blur(function (e) {
                currentSelection = -1;
                //proposalList.empty();
                params.onBlur();
            });

            searchContainer.append(input);
            searchContainer.append(proposals);

            if (params.showButton) {
                //Search button
                var button = $('<input type="submit" value="search"></input>')
                    .attr("style", "width: 100px;\n" +
                        "    height: 42px;\n" +
                        "    background: green;\n" +
                        "    border: 0px;\n" +
                        "    float: left;\n" +
                        "    color: white;\n" +
                        "    cursor: pointer;")
                    .html("search")
                    .css({
                        'height': "42px",
                        'line-height': "42px"
                    })
                    .click(function () {
                        proposalList.empty();
                        params.onSubmit(input.val());
                    });
                searchContainer.append(button);
            }

            $(this).append(searchContainer);

            if (params.showButton) {
                //Width fix
                searchContainer.css('width', params.width + button.width() + 150);
            }
        });

        return this;
    };

})(jQuery);