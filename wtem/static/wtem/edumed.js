// Generated by CoffeeScript 1.6.3
(function() {
  var $, Binding, EduModule, Exercise, Luki, PrawdaFalsz, Przyporzadkuj, Uporzadkuj, Wybor, Zastap, exercise,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  $ = jQuery;

  Binding = (function() {
    function Binding(handler, element) {
      this.handler = handler;
      this.element = element;
      $(this.element).data(this.handler, this);
    }

    return Binding;

  })();

  EduModule = (function(_super) {
    __extends(EduModule, _super);

    function EduModule(element) {
      EduModule.__super__.constructor.call(this, 'edumodule', element);
    }

    return EduModule;

  })(Binding);

  Exercise = (function(_super) {
    __extends(Exercise, _super);

    function Exercise(element) {
      var _this = this;
      Exercise.__super__.constructor.call(this, 'exercise', element);
      $(this.element).data("exercise-html", $(this.element).html());
      $(".check", this.element).click(function(ev) {
        _this.check();
        $(".retry", _this.element).show();
        return $(".check", _this.element).hide();
      });
      $(".retry", this.element).click(function(ev) {
        return _this.retry();
      });
      $('.solutions', this.element).click(function() {
        _this.show_solutions();
        return $(".comment", _this.element).show();
      });
      $('.reset', this.element).click(function() {
        return _this.reset();
      });
    }

    Exercise.prototype.retry = function() {
      $(".correct, .incorrect", this.element).removeClass("correct incorrect");
      $(".check", this.element).show();
      return $(".retry", this.element).hide();
    };

    Exercise.prototype.reset = function() {
      $(this.element).html($(this.element).data('exercise-html'));
      return exercise(this.element);
    };

    Exercise.prototype.piece_correct = function(qpiece) {
      return $(qpiece).removeClass('incorrect').addClass('correct');
    };

    Exercise.prototype.piece_incorrect = function(qpiece) {
      return $(qpiece).removeClass('correct').addClass('incorrect');
    };

    Exercise.prototype.check = function() {
      var score, scores,
        _this = this;
      scores = [];
      $(".question", this.element).each(function(i, question) {
        return scores.push(_this.check_question(question));
      });
      score = [0, 0, 0];
      $.each(scores, function(i, s) {
        score[0] += s[0];
        score[1] += s[1];
        return score[2] += s[2];
      });
      return this.show_score(score);
    };

    Exercise.prototype.show_solutions = function() {
      var _this = this;
      this.reset();
      return $(".question", this.element).each(function(i, question) {
        return _this.solve_question(question);
      });
    };

    Exercise.prototype.get_answers = function() {
      var answers,
        _this = this;
      answers = [];
      $('.question', this.element).each(function(i, question) {
        return answers.push(_this.get_answer(question));
      });
      return answers;
    };

    Exercise.prototype.get_value_list = function(elem, data_key, numbers) {
      var vl;
      vl = $(elem).attr("data-" + data_key).split(/[ ,]+/).map($.trim);
      if (numbers) {
        vl = vl.map(function(x) {
          return parseInt(x);
        });
      }
      return vl;
    };

    Exercise.prototype.get_value_optional_list = function(elem, data_key) {
      var mandat, opt, v, vals, _i, _len;
      vals = this.get_value_list(elem, data_key);
      mandat = [];
      opt = [];
      for (_i = 0, _len = vals.length; _i < _len; _i++) {
        v = vals[_i];
        if (v.slice(-1) === "?") {
          opt.push(v.slice(0, -1));
        } else {
          mandat.push(v);
        }
      }
      return [mandat, opt];
    };

    Exercise.prototype.show_score = function(score) {
      var $msg;
      $msg = $(".message", this.element);
      $msg.text("Wynik: " + score[0] + " / " + score[2]);
      if (score[0] >= score[2] && score[1] === 0) {
        return $msg.addClass("maxscore");
      } else {
        return $msg.removeClass("maxscore");
      }
    };

    Exercise.prototype.draggable_equal = function($draggable1, $draggable2) {
      return false;
    };

    Exercise.prototype.draggable_accept = function($draggable, $droppable) {
      var d, dropped, _i, _len;
      dropped = $droppable.closest("ul, ol").find(".draggable");
      for (_i = 0, _len = dropped.length; _i < _len; _i++) {
        d = dropped[_i];
        if (this.draggable_equal($draggable, $(d))) {
          return false;
        }
      }
      return true;
    };

    Exercise.prototype.draggable_move = function($draggable, $placeholder, ismultiple) {
      var $added,
        _this = this;
      $added = $draggable.clone();
      $added.data("original", $draggable.get(0));
      if (!ismultiple) {
        $draggable.addClass('disabled').draggable('disable');
      }
      $placeholder.after($added);
      if (!$placeholder.hasClass('multiple')) {
        $placeholder.hide();
      }
      if ($added.is(".add-li")) {
        $added.wrap("<li/>");
      }
      $added.append('<span class="remove">x</span><div class="clr"></div>');
      return $('.remove', $added).click(function(ev) {
        _this.retry();
        if (!ismultiple) {
          $($added.data('original')).removeClass('disabled').draggable('enable');
        }
        if ($added.is(".add-li")) {
          $added = $added.closest('li');
        }
        $added.prev(".placeholder:not(.multiple)").show();
        return $added.remove();
      });
    };

    Exercise.prototype.dragging = function(ismultiple, issortable) {
      var _this = this;
      return $(".question", this.element).each(function(i, question) {
        var draggable_opts, self;
        draggable_opts = {
          revert: 'invalid',
          helper: 'clone',
          start: _this.retry
        };
        $(".draggable", question).draggable(draggable_opts);
        self = _this;
        return $(".placeholder", question).droppable({
          accept: function(draggable) {
            var $draggable, is_accepted;
            $draggable = $(draggable);
            is_accepted = true;
            if (!$draggable.is(".draggable")) {
              is_accepted = false;
            }
            if (is_accepted) {
              is_accepted = self.draggable_accept($draggable, $(this));
            }
            if (is_accepted) {
              $(this).addClass('accepting');
            } else {
              $(this).removeClass('accepting');
            }
            return is_accepted;
          },
          drop: function(ev, ui) {
            $(ev.target).removeClass('accepting dragover');
            return _this.draggable_move($(ui.draggable), $(ev.target), ismultiple);
          },
          over: function(ev, ui) {
            return $(ev.target).addClass('dragover');
          },
          out: function(ev, ui) {
            return $(ev.target).removeClass('dragover');
          }
        });
      });
    };

    return Exercise;

  })(Binding);

  Wybor = (function(_super) {
    __extends(Wybor, _super);

    function Wybor(element) {
      Wybor.__super__.constructor.call(this, element);
      $(".question-piece input", element).change(this.retry);
    }

    Wybor.prototype.check_question = function(question) {
      var all, bad, good, solution,
        _this = this;
      all = 0;
      good = 0;
      bad = 0;
      solution = this.get_value_list(question, 'solution');
      $(".question-piece", question).each(function(i, qpiece) {
        var is_checked, piece_name, piece_no, should_be_checked;
        piece_no = $(qpiece).attr('data-no');
        piece_name = $(qpiece).attr('data-name');
        if (piece_name) {
          should_be_checked = solution.indexOf(piece_name) >= 0;
        } else {
          should_be_checked = solution.indexOf(piece_no) >= 0;
        }
        is_checked = $("input", qpiece).is(":checked");
        if (should_be_checked) {
          all += 1;
        }
        if (is_checked) {
          if (should_be_checked) {
            good += 1;
            return _this.piece_correct(qpiece);
          } else {
            bad += 1;
            return _this.piece_incorrect(qpiece);
          }
        } else {
          return $(qpiece).removeClass("correct,incorrect");
        }
      });
      return [good, bad, all];
    };

    Wybor.prototype.solve_question = function(question) {
      var solution,
        _this = this;
      solution = this.get_value_list(question, 'solution');
      return $(".question-piece", question).each(function(i, qpiece) {
        var piece_name, piece_no, should_be_checked;
        piece_no = $(qpiece).attr('data-no');
        piece_name = $(qpiece).attr('data-name');
        if (piece_name) {
          should_be_checked = solution.indexOf(piece_name) >= 0;
        } else {
          should_be_checked = solution.indexOf(piece_no) >= 0;
        }
        console.log("check " + $("input[type=checkbox]", qpiece).attr("id") + " -> " + should_be_checked);
        return $("input[type=checkbox],input[type=radio]", qpiece).prop('checked', should_be_checked);
      });
    };

    Wybor.prototype.get_answer = function(question) {
      var answer,
        _this = this;
      answer = [];
      $('.question-piece', question).each(function(i, qpiece) {
        var $qpiece;
        $qpiece = $(qpiece);
        if ($("input[type=checkbox],input[type=radio]", qpiece).is(':checked')) {
          return answer.push($qpiece.attr('data-name'));
        }
      });
      return answer;
    };

    return Wybor;

  })(Exercise);

  Uporzadkuj = (function(_super) {
    __extends(Uporzadkuj, _super);

    function Uporzadkuj(element) {
      Uporzadkuj.__super__.constructor.call(this, element);
      $('ol, ul', this.element).sortable({
        items: "> li",
        start: this.retry
      });
    }

    Uporzadkuj.prototype.check_question = function(question) {
      var all, bad, correct, pkt, pkts, positions, sorted, _i, _ref;
      positions = this.get_value_list(question, 'original', true);
      sorted = positions.sort();
      pkts = $('.question-piece', question);
      correct = 0;
      bad = 0;
      all = 0;
      for (pkt = _i = 0, _ref = pkts.length; 0 <= _ref ? _i < _ref : _i > _ref; pkt = 0 <= _ref ? ++_i : --_i) {
        all += 1;
        if (pkts.eq(pkt).data('pos') === sorted[pkt]) {
          correct += 1;
          this.piece_correct(pkts.eq(pkt));
        } else {
          bad += 1;
          this.piece_incorrect(pkts.eq(pkt));
        }
      }
      return [correct, bad, all];
    };

    Uporzadkuj.prototype.solve_question = function(question) {
      var p, parent, pkts, positions, sorted, _i, _len, _results;
      positions = this.get_value_list(question, 'original', true);
      sorted = positions.sort();
      pkts = $('.question-piece', question);
      pkts.sort(function(a, b) {
        var q, w;
        q = $(a).data('pos');
        w = $(b).data('pos');
        if (q < w) {
          return 1;
        }
        if (q > w) {
          return -1;
        }
        return 0;
      });
      parent = pkts.eq(0).parent();
      _results = [];
      for (_i = 0, _len = pkts.length; _i < _len; _i++) {
        p = pkts[_i];
        _results.push(parent.prepend(p));
      }
      return _results;
    };

    return Uporzadkuj;

  })(Exercise);

  Luki = (function(_super) {
    __extends(Luki, _super);

    function Luki(element) {
      Luki.__super__.constructor.call(this, element);
      this.dragging(false, false);
    }

    Luki.prototype.check = function() {
      var all, bad, correct,
        _this = this;
      all = $(".placeholder", this.element).length;
      correct = 0;
      bad = 0;
      $(".placeholder + .question-piece", this.element).each(function(i, qpiece) {
        var $placeholder;
        $placeholder = $(qpiece).prev(".placeholder");
        if ($placeholder.data('solution') === $(qpiece).data('no')) {
          _this.piece_correct(qpiece);
          return correct += 1;
        } else {
          bad += 1;
          return _this.piece_incorrect(qpiece);
        }
      });
      return this.show_score([correct, bad, all]);
    };

    Luki.prototype.solve_question = function(question) {
      var _this = this;
      return $(".placeholder", question).each(function(i, placeholder) {
        var $qp;
        $qp = $(".question-piece[data-no=" + $(placeholder).data('solution') + "]", question);
        return _this.draggable_move($qp, $(placeholder), false);
      });
    };

    return Luki;

  })(Exercise);

  Zastap = (function(_super) {
    __extends(Zastap, _super);

    function Zastap(element) {
      var _this = this;
      Zastap.__super__.constructor.call(this, element);
      $(".paragraph", this.element).each(function(i, par) {
        return _this.wrap_words($(par), $('<span class="placeholder zastap"/>'));
      });
      this.dragging(false, false);
    }

    Zastap.prototype.check = function() {
      var all, bad, correct,
        _this = this;
      all = 0;
      correct = 0;
      bad = 0;
      $(".paragraph", this.element).each(function(i, par) {
        return $(".placeholder", par).each(function(j, qpiece) {
          var $dragged, $qp;
          $qp = $(qpiece);
          $dragged = $qp.next(".draggable");
          if ($qp.data("solution")) {
            if ($dragged && $qp.data("solution") === $dragged.data("no")) {
              _this.piece_correct($dragged);
              correct += 1;
            }
            return all += 1;
          }
        });
      });
      return this.show_score([correct, bad, all]);
    };

    Zastap.prototype.show_solutions = function() {
      var _this = this;
      this.reset();
      return $(".paragraph", this.element).each(function(i, par) {
        return $(".placeholder[data-solution]", par).each(function(j, qpiece) {
          var $dr, $qp;
          $qp = $(qpiece);
          $dr = $(".draggable[data-no=" + $qp.data('solution') + "]", _this.element);
          return _this.draggable_move($dr, $qp, false);
        });
      });
    };

    Zastap.prototype.wrap_words = function(element, wrapper) {
      var chld, i, ignore, insertWrapped, j, len, space, wordb, _i, _ref, _results;
      ignore = /^[ \t.,:;()]+/;
      insertWrapped = function(txt, elem) {
        var nw;
        nw = wrapper.clone();
        return $(document.createTextNode(txt)).wrap(nw).parent().attr("data-original", txt).insertBefore(elem);
      };
      _results = [];
      for (j = _i = _ref = element.get(0).childNodes.length - 1; _ref <= 0 ? _i <= 0 : _i >= 0; j = _ref <= 0 ? ++_i : --_i) {
        chld = element.get(0).childNodes[j];
        if (chld.nodeType === document.TEXT_NODE) {
          len = chld.textContent.length;
          wordb = 0;
          i = 0;
          while (i < len) {
            space = ignore.exec(chld.textContent.substr(i));
            if (space != null) {
              if (wordb < i) {
                insertWrapped(chld.textContent.substr(wordb, i - wordb), chld);
              }
              $(document.createTextNode(space[0])).insertBefore(chld);
              i += space[0].length;
              wordb = i;
            } else {
              i = i + 1;
            }
          }
          if (wordb < len - 1) {
            insertWrapped(chld.textContent.substr(wordb, len - 1 - wordb), chld);
          }
          _results.push($(chld).remove());
        } else {
          _results.push(void 0);
        }
      }
      return _results;
    };

    return Zastap;

  })(Exercise);

  Przyporzadkuj = (function(_super) {
    __extends(Przyporzadkuj, _super);

    Przyporzadkuj.prototype.is_multiple = function() {
      var qp, _i, _len, _ref;
      _ref = $(".question-piece", this.element);
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        qp = _ref[_i];
        if ($(qp).attr('data-solution').split(/[ ,]+/).length > 1) {
          return true;
        }
      }
      return false;
    };

    function Przyporzadkuj(element) {
      Przyporzadkuj.__super__.constructor.call(this, element);
      this.multiple = this.is_multiple();
      this.dragging(this.multiple, true);
    }

    Przyporzadkuj.prototype.draggable_equal = function(d1, d2) {
      return d1.data("no") === d2.data("no");
    };

    Przyporzadkuj.prototype.check_question = function(question) {
      var all, bad_count, count, mandatory, minimum, optional, pn, pred, qp, self, v, _i, _j, _len, _len1, _ref, _ref1;
      minimum = $(question).data("minimum");
      count = 0;
      bad_count = 0;
      all = 0;
      if (!minimum) {
        self = this;
        $(".subject .question-piece", question).each(function(i, el) {
          var mandatory, v;
          v = self.get_value_optional_list(el, 'solution');
          mandatory = v[0];
          return all += mandatory.length;
        });
      }
      _ref = $(".predicate [data-predicate]", question);
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        pred = _ref[_i];
        pn = $(pred).attr('data-predicate');
        _ref1 = $(".question-piece", pred);
        for (_j = 0, _len1 = _ref1.length; _j < _len1; _j++) {
          qp = _ref1[_j];
          v = this.get_value_optional_list(qp, 'solution');
          mandatory = v[0];
          optional = v[1];
          if (mandatory.indexOf(pn) >= 0 || (minimum && optional.indexOf(pn) >= 0)) {
            count += 1;
            this.piece_correct(qp);
          } else {
            bad_count += 1;
            this.piece_incorrect(qp);
          }
        }
      }
      return [count, bad_count, all];
    };

    Przyporzadkuj.prototype.solve_question = function(question) {
      var $ph, $pr, draggables, m, mandatory, minimum, optional, qp, v, _i, _len, _ref, _results;
      minimum = $(question).data("min");
      _ref = $(".subject .question-piece", question);
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        qp = _ref[_i];
        v = this.get_value_optional_list(qp, 'solution');
        mandatory = v[0];
        optional = v[1];
        if (minimum) {
          draggables = mandatory.count(optional).slice(0, minimum);
        } else {
          draggables = mandatory;
        }
        _results.push((function() {
          var _j, _len1, _results1;
          _results1 = [];
          for (_j = 0, _len1 = draggables.length; _j < _len1; _j++) {
            m = draggables[_j];
            $pr = $(".predicate [data-predicate=" + m + "]", question);
            $ph = $pr.find(".placeholder:visible");
            _results1.push(this.draggable_move($(qp), $ph.eq(0), this.multiple));
          }
          return _results1;
        }).call(this));
      }
      return _results;
    };

    Przyporzadkuj.prototype.get_answer = function(question) {
      var answer,
        _this = this;
      answer = {};
      $(".predicate [data-predicate]", question).each(function(i, subjects) {
        var predicate;
        predicate = $(subjects).attr('data-predicate');
        answer[predicate] = [];
        return $('.question-piece', subjects).each(function(i, qpiece) {
          var $qpiece;
          $qpiece = $(qpiece);
          return answer[predicate].push($qpiece.attr('data-id'));
        });
      });
      return answer;
    };

    return Przyporzadkuj;

  })(Exercise);

  PrawdaFalsz = (function(_super) {
    __extends(PrawdaFalsz, _super);

    function PrawdaFalsz(element) {
      var qp, _i, _len, _ref,
        _this = this;
      PrawdaFalsz.__super__.constructor.call(this, element);
      _ref = $(".question-piece", this.element);
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        qp = _ref[_i];
        $(".true", qp).click(function(ev) {
          ev.preventDefault();
          _this.retry();
          $(ev.target).closest(".question-piece").data("value", "true");
          return $(ev.target).addClass('chosen').siblings('a').removeClass('chosen');
        });
        $(".false", qp).click(function(ev) {
          ev.preventDefault();
          _this.retry();
          $(ev.target).closest(".question-piece").data("value", "false");
          return $(ev.target).addClass('chosen').siblings('a').removeClass('chosen');
        });
      }
    }

    PrawdaFalsz.prototype.check_question = function() {
      var all, bad, good, qp, _i, _len, _ref;
      all = 0;
      good = 0;
      bad = 0;
      _ref = $(".question-piece", this.element);
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        qp = _ref[_i];
        if ($(qp).data("solution").toString() === $(qp).data("value")) {
          good += 1;
          this.piece_correct(qp);
        } else {
          bad += 1;
          this.piece_incorrect(qp);
        }
        all += 1;
      }
      return [good, bad, all];
    };

    PrawdaFalsz.prototype.show_solutions = function() {
      var qp, _i, _len, _ref, _results;
      this.reset();
      _ref = $(".question-piece", this.element);
      _results = [];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        qp = _ref[_i];
        if ($(qp).data('solution') === true) {
          _results.push($(".true", qp).click());
        } else {
          _results.push($(".false", qp).click());
        }
      }
      return _results;
    };

    PrawdaFalsz.prototype.get_answer = function(question) {
      var answer,
        _this = this;
      answer = [];
      $(".question-piece", this.element).each(function(i, qpiece) {
        return answer.push($(qpiece).data('value') || '-');
      });
      return answer;
    };

    return PrawdaFalsz;

  })(Exercise);

  exercise = function(ele) {
    var cls, es;
    es = {
      wybor: Wybor,
      uporzadkuj: Uporzadkuj,
      luki: Luki,
      zastap: Zastap,
      przyporzadkuj: Przyporzadkuj,
      prawdafalsz: PrawdaFalsz
    };
    cls = es[$(ele).attr('data-type')];
    return new cls(ele);
  };

  window.edumed = {
    'EduModule': EduModule
  };

  $(document).ready(function() {
    new EduModule($("#book-text"));
    return $(".exercise").each(function(i, el) {
      return exercise(this);
    });
  });

}).call(this);
