    // **analyze**
    //
    // The main body of the rhyme analysis algorithm
    function analyze(tune){
        var loader = document.getElementById('loadloadloading');
        if(loader){
            loader.className = "active loadloadloading";
        }
        var theUserviz = document.getElementById('tunes-userviz');
        if(theUserviz){
            theUserviz.className += " faded";
        }
        var theUserVizError = document.getElementById('tunes-userviz-error');
        if(theUserVizError){
            theUserVizError.className = "hidden";
        }
        $('#tunes-userviz').removeClass('hidden');

        window.setTimeout(function(){
            if(typeof(tune) === "undefined"){
                tune = false;
            }
            
            // Load lyrics, split them into words and look them up in the pronunciation 
            // dictionary
            var lyrics = document.getElementById("lyrics").value.split("\n"),
                process = processText(lyrics.concat(["xxx"])),
                sounds = process[0],
                syllables = _.flatten(process[1]),
                words = process[2];

            // Determine if any words couldn't be looked up
            var missing_words = _.some(words,function(w){
                return w.pros.length === 0 && w.word != "xxx";
            });

            // Adjust for a strictness parameter
            mcl_param = document.getElementById("fader").value;
            window.SCALE = (mcl_param - 2)/3.5;

            // Put each syllable into a dictionary based on its label for easy
            // debugging and crossreference
            syl_dict = {};
            _.each(syllables,function(s,i){
                syl_dict[s.label()] = s;
            });

            // Assign each syllables its neighbors
            findNeighbors(words);

            // Assign each syllables its scored rhymes
            var G = findMatches(words);

            // Pick which pronunciations to use
            var winners = pickWinners(sounds),
                reduced_syls = winners[0],
                flat_syls = winners[1];

            // Run our first clustering into rhyme families
            var first_mcl = createMCL(flat_syls,G,2 + SCALE);
            var partition = makeClusters(syl_dict,G,first_mcl);
            clusterColor(partition);
            var groups = cleanFinalColors(flat_syls,G,syl_dict);

            var final_mcl,final_partition,final_groups;

            // Cluster an additional two times, pruning the graph between steps,
            // allowing the clustering to feedback into the graph and remove and weaken
            // contextually-weak rhymes
            _(2).times(function(){
                pruneGraph(G,groups,syl_dict);
                final_mcl = createMCL(flat_syls,G,2 + SCALE);
                final_partition = makeClusters(syl_dict,G,final_mcl);
                clusterColor(final_partition);
                final_groups = cleanFinalColors(flat_syls,G,syl_dict);
            });

            final_reduced_syls = assignRealSyls(reduced_syls,sounds);
            final_reduced_syls = final_reduced_syls.slice(0,-1);
            var csv = writeArray(final_reduced_syls,flat_syls);
            if(tune && tune !== -1){
                var userviz = new tune({
                    source:'',
                    file:'userviz',
                    title:'',
                    artist:'',
                    album:'',
                    data:csv,
                    show:true,
                    music:false,
                    container:'userviz',
                    missing_words: missing_words
                  });
            } else if (tune === -1) {
                showColors(final_reduced_syls,flat_syls);
            }
            //console.log(JSON.stringify(csv))
            //console.log("MISSING",missing_words)
                $('#tunes-userviz').removeClass('nada');
            $('#loadloadloading').removeClass('active');
            $('#tunes-userviz').removeClass('faded');

            if($('#tunes-userviz g[data-row=1]').length===0){
                console.log('nada');
                $('#tunes-userviz').addClass('hidden nada');
                $('#tunes-userviz-error').removeClass('hidden');
            }

            return csv;
        }, 500);

    }
