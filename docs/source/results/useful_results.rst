Experimental Results
==============


We have undertaken rigorous evaluations of BC, BCQ-MA, CQL-MA, ICQ-MA, and MADT on the D4MARL dataset. Multiple metrics have been amassed and juxtaposed. The intricacies of these experiments are elaborated comprehensively in our paper. We anticipate that forthcoming algorithms in the SMAC domain will leverage our D4MARL dataset, facilitating comparisons within a unified framework.

.. raw:: html

    <link rel="stylesheet" type="text/css" href="../_static/table.css">
    <link rel="stylesheet" type="text/css" href="../_static/clean-blog.css">

    <div class="col-lg-12">
        <div class="card card-outline-secondary w-100">
            <div class="card-header">
                Experimental Results on D4MARL
            </div>
            <div class="card-body">
                In the presented table, we showcase the empirical outcomes of diverse algorithms applied to the D4MARL dataset. As additional algorithms are proposed and evaluated on the D4MARL dataset, we will continuously update this leaderboard with their results.
                <table class="table table-responsive">
                    <thead class="thead-light">
                        <!-- Header Row -->
                        <tr>
                            <th scope="col" rowspan="2" class="align-middle text-center">Map Name</th>
                            <th scope="col" rowspan="2" class="align-middle text-center">Quality</th>
                            <th scope="col" class="align-middle text-center">Method</th>
                            <th scope="col" colspan="2" class="align-middle text-center">Static Accuracy (%)</th>
                            <th scope="col" rowspan="2" class="align-middle text-center">Return</th>
                            <th scope="col" rowspan="2" class="align-middle text-center">Win Rate</th>
                            <th scope="col" rowspan="2" class="align-middle text-center">Time-to-Threshold</th>
                        </tr>
                        <tr>
                            <th scope="col" class="align-middle text-center"></th>
                            <th scope="col" class="align-middle text-center">SA_dev</th>
                            <th scope="col" class="align-middle text-center">SA_test</th>
                        </tr>
                    </thead>
                    <tbody>

                        <tr>
                            <td rowspan="15" class="align-middle text-center">2m_vs_1z</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">73.68</td>
                            <td class="align-middle text-center">71.46</td>
                            <td class="align-middle text-center">3.95</td>
                            <td class="align-middle text-center">0.98</td>
                            <td class="align-middle text-center">--</td>
                        </tr>

                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">40.12</td>
                            <td class="align-middle text-center">40.69</td>
                            <td class="align-middle text-center">17.97</td>
                            <td class="align-middle text-center">84.01</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">9.23</td>
                            <td class="align-middle text-center">9.41</td>
                            <td class="align-middle text-center">18.61</td>
                            <td class="align-middle text-center">90.90</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">58.81</td>
                            <td class="align-middle text-center">59.25</td>
                            <td class="align-middle text-center">19.19</td>
                            <td class="align-middle text-center">93.84</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">50.91</td>
                            <td class="align-middle text-center">50.73</td>
                            <td class="align-middle text-center">19.59</td>
                            <td class="align-middle text-center">97.12</td>
                            <td class="align-middle text-center">1.886</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">71.34</td>
                            <td class="align-middle text-center">73.54</td>
                            <td class="align-middle text-center">3.96</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">51.96</td>
                            <td class="align-middle text-center">49.47</td>
                            <td class="align-middle text-center">14.47</td>
                            <td class="align-middle text-center">59.38</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">9.44</td>
                            <td class="align-middle text-center">10.96</td>
                            <td class="align-middle text-center">8.47</td>
                            <td class="align-middle text-center">21.62</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">64.79</td>
                            <td class="align-middle text-center">65.09</td>
                            <td class="align-middle text-center">16.87</td>
                            <td class="align-middle text-center">78.99</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">49.82</td>
                            <td class="align-middle text-center">49.10</td>
                            <td class="align-middle text-center">18.24</td>
                            <td class="align-middle text-center">86.27</td>
                            <td class="align-middle text-center">1.643</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">71.62</td>
                            <td class="align-middle text-center">71.71</td>
                            <td class="align-middle text-center">3.683</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                       <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">63.10</td>
                            <td class="align-middle text-center">67.78</td>
                            <td class="align-middle text-center">5.57</td>
                            <td class="align-middle text-center">0.06</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">37.02</td>
                            <td class="align-middle text-center">32.18</td>
                            <td class="align-middle text-center">6.20</td>
                            <td class="align-middle text-center">1.01</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">35.52</td>
                            <td class="align-middle text-center">40.99</td>
                            <td class="align-middle text-center">8.948</td>
                            <td class="align-middle text-center">18.56</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">56.46</td>
                            <td class="align-middle text-center">55.59</td>
                            <td class="align-middle text-center">5.43</td>
                            <td class="align-middle text-center">2.45</td>
                            <td class="align-middle text-center">6.749</td>
                        </tr>

                        <tr>
                            <td rowspan="15" class="align-middle text-center">2s_vs_1sc</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">91.95</td>
                            <td class="align-middle text-center">91.81</td>
                            <td class="align-middle text-center">15.63</td>
                            <td class="align-middle text-center">53.95</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">63.10</td>
                            <td class="align-middle text-center">63.81</td>
                            <td class="align-middle text-center">19.99</td>
                            <td class="align-middle text-center">98.01</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">78.40</td>
                            <td class="align-middle text-center">78.35</td>
                            <td class="align-middle text-center">19.89</td>
                            <td class="align-middle text-center">95.97</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">16.41</td>
                            <td class="align-middle text-center">18.77</td>
                            <td class="align-middle text-center">20.16</td>
                            <td class="align-middle text-center">99.28</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">73.85</td>
                            <td class="align-middle text-center">71.10</td>
                            <td class="align-middle text-center">20.24</td>
                            <td class="align-middle text-center">99.97</td>
                            <td class="align-middle text-center">0.2597</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">90.33</td>
                            <td class="align-middle text-center">91.41</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">73.64</td>
                            <td class="align-middle text-center">74.85</td>
                            <td class="align-middle text-center">19.85</td>
                            <td class="align-middle text-center">95.10</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">82.60</td>
                            <td class="align-middle text-center">85.04</td>
                            <td class="align-middle text-center">13.26</td>
                            <td class="align-middle text-center">15.71</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">22.44</td>
                            <td class="align-middle text-center">22.69</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">71.57</td>
                            <td class="align-middle text-center">73.04</td>
                            <td class="align-middle text-center">19.74</td>
                            <td class="align-middle text-center">94.49</td>
                            <td class="align-middle text-center">1.211</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">74.14</td>
                            <td class="align-middle text-center">57.77</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">70.71</td>
                            <td class="align-middle text-center">61.86</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">68.82</td>
                            <td class="align-middle text-center">57.35</td>
                            <td class="align-middle text-center">8.79</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">17.73</td>
                            <td class="align-middle text-center">33.58</td>
                            <td class="align-middle text-center">0.42</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">49.64</td>
                            <td class="align-middle text-center">50.88</td>
                            <td class="align-middle text-center">17.48</td>
                            <td class="align-middle text-center">68.24</td>
                            <td class="align-middle text-center">2.724</td>
                        </tr>

                        <tr>
                            <td rowspan="10" class="align-middle text-center">3m</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">91.39</td>
                            <td class="align-middle text-center">89.47</td>
                            <td class="align-middle text-center">14.36</td>
                            <td class="align-middle text-center">55.07</td>
                            <td class="align-middle text-center">0.1607</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">75.91</td>
                            <td class="align-middle text-center">71.58</td>
                            <td class="align-middle text-center">15.86</td>
                            <td class="align-middle text-center">66.98</td>
                            <td class="align-middle text-center">0.1430</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">13.94</td>
                            <td class="align-middle text-center">15.36</td>
                            <td class="align-middle text-center">11.66</td>
                            <td class="align-middle text-center">33.67</td>
                            <td class="align-middle text-center">0.2209</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">27.75</td>
                            <td class="align-middle text-center">30.60</td>
                            <td class="align-middle text-center">15.93</td>
                            <td class="align-middle text-center">68.22</td>
                            <td class="align-middle text-center">0.2332</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">78.13</td>
                            <td class="align-middle text-center">78.40</td>
                            <td class="align-middle text-center">19.59</td>
                            <td class="align-middle text-center">96.88</td>
                            <td class="align-middle text-center">0.1223</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">80.30</td>
                            <td class="align-middle text-center">81.49</td>
                            <td class="align-middle text-center">14.11</td>
                            <td class="align-middle text-center">52.47</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">74.35</td>
                            <td class="align-middle text-center">73.28</td>
                            <td class="align-middle text-center">13.81</td>
                            <td class="align-middle text-center">49.56</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">51.11</td>
                            <td class="align-middle text-center">53.38</td>
                            <td class="align-middle text-center">0.45</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">18.06</td>
                            <td class="align-middle text-center">22.21</td>
                            <td class="align-middle text-center">14.68</td>
                            <td class="align-middle text-center">59.15</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">68.36</td>
                            <td class="align-middle text-center">74.04</td>
                            <td class="align-middle text-center">15.15</td>
                            <td class="align-middle text-center">63.01</td>
                            <td class="align-middle text-center">0.1554</td>
                        </tr>


                        <tr>
                            <td rowspan="15" class="align-middle text-center">2s3z</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">78.01</td>
                            <td class="align-middle text-center">71.79</td>
                            <td class="align-middle text-center">15.73</td>
                            <td class="align-middle text-center">34.35</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">76.15</td>
                            <td class="align-middle text-center">73.14</td>
                            <td class="align-middle text-center">19.03</td>
                            <td class="align-middle text-center">83.42</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">22.30</td>
                            <td class="align-middle text-center">21.41</td>
                            <td class="align-middle text-center">18.73</td>
                            <td class="align-middle text-center">77.04</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">14.99</td>
                            <td class="align-middle text-center">14.68</td>
                            <td class="align-middle text-center">17.59</td>
                            <td class="align-middle text-center">60.58</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">58.59</td>
                            <td class="align-middle text-center">60.04</td>
                            <td class="align-middle text-center">19.93</td>
                            <td class="align-middle text-center">98.61</td>
                            <td class="align-middle text-center">0.2907</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">75.99</td>
                            <td class="align-middle text-center">73.27</td>
                            <td class="align-middle text-center">13.20</td>
                            <td class="align-middle text-center">16.48</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">75.69</td>
                            <td class="align-middle text-center">74.54</td>
                            <td class="align-middle text-center">17.64</td>
                            <td class="align-middle text-center">62.39</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">27.45</td>
                            <td class="align-middle text-center">26.05</td>
                            <td class="align-middle text-center">15.91</td>
                            <td class="align-middle text-center">40.01</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">15.66</td>
                            <td class="align-middle text-center">15.61</td>
                            <td class="align-middle text-center">13.22</td>
                            <td class="align-middle text-center">17.33</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">54.67</td>
                            <td class="align-middle text-center">52.89</td>
                            <td class="align-middle text-center">18.66</td>
                            <td class="align-middle text-center">80.66</td>
                            <td class="align-middle text-center">0.3246</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">74.02</td>
                            <td class="align-middle text-center">72.74</td>
                            <td class="align-middle text-center">7.61</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">73.83</td>
                            <td class="align-middle text-center">72.35</td>
                            <td class="align-middle text-center">9.57</td>
                            <td class="align-middle text-center">8.20</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">45.02</td>
                            <td class="align-middle text-center">39.98</td>
                            <td class="align-middle text-center">6.65</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">6.71</td>
                            <td class="align-middle text-center">7.21</td>
                            <td class="align-middle text-center">7.26</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">56.49</td>
                            <td class="align-middle text-center">55.94</td>
                            <td class="align-middle text-center">14.39</td>
                            <td class="align-middle text-center">25.29</td>
                            <td class="align-middle text-center">58.97</td>
                        </tr>

                        <tr>
                            <td rowspan="15" class="align-middle text-center">3s_vs_3z</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">64.13</td>
                            <td class="align-middle text-center">63.46</td>
                            <td class="align-middle text-center">8.77</td>
                            <td class="align-middle text-center">9.38</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">45.03</td>
                            <td class="align-middle text-center">44.96</td>
                            <td class="align-middle text-center">18.90</td>
                            <td class="align-middle text-center">82.40</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">6.79</td>
                            <td class="align-middle text-center">6.10</td>
                            <td class="align-middle text-center">15.78</td>
                            <td class="align-middle text-center">42.30</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">13.06</td>
                            <td class="align-middle text-center">12.60</td>
                            <td class="align-middle text-center">17.15</td>
                            <td class="align-middle text-center">62.63</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">54.34</td>
                            <td class="align-middle text-center">52.73</td>
                            <td class="align-middle text-center">19.21</td>
                            <td class="align-middle text-center">84.25</td>
                            <td class="align-middle text-center">0.3778</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">61.71</td>
                            <td class="align-middle text-center">59.85</td>
                            <td class="align-middle text-center">6.41</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">52.36</td>
                            <td class="align-middle text-center">51.17</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">9.42</td>
                            <td class="align-middle text-center">5.72</td>
                            <td class="align-middle text-center">8.93</td>
                            <td class="align-middle text-center">1.52</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">12.37</td>
                            <td class="align-middle text-center">13.35</td>
                            <td class="align-middle text-center">11.12</td>
                            <td class="align-middle text-center">14.66</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">47.25</td>
                            <td class="align-middle text-center">47.33</td>
                            <td class="align-middle text-center">9.26</td>
                            <td class="align-middle text-center">5.18</td>
                            <td class="align-middle text-center">21.26</td>
                        </tr>

                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">74.02</td>
                            <td class="align-middle text-center">72.74</td>
                            <td class="align-middle text-center">7.61</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">73.83</td>
                            <td class="align-middle text-center">72.35</td>
                            <td class="align-middle text-center">9.57</td>
                            <td class="align-middle text-center">8.20</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">45.02</td>
                            <td class="align-middle text-center">39.98</td>
                            <td class="align-middle text-center">6.65</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">6.71</td>
                            <td class="align-middle text-center">7.21</td>
                            <td class="align-middle text-center">7.26</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">52.50</td>
                            <td class="align-middle text-center">52.12</td>
                            <td class="align-middle text-center">9.62</td>
                            <td class="align-middle text-center">0.25</td>
                            <td class="align-middle text-center">61.49</td>
                        </tr>


                        <!-- 3s_vs_4z Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">3s_vs_4z</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">69.78</td>
                            <td class="align-middle text-center">66.71</td>
                            <td class="align-middle text-center">8.74</td>
                            <td class="align-middle text-center">2.27</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">28.81</td>
                            <td class="align-middle text-center">28.92</td>
                            <td class="align-middle text-center">18.78</td>
                            <td class="align-middle text-center">78.26</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">13.42</td>
                            <td class="align-middle text-center">15.48</td>
                            <td class="align-middle text-center">11.67</td>
                            <td class="align-middle text-center">11.64</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">13.08</td>
                            <td class="align-middle text-center">12.59</td>
                            <td class="align-middle text-center">13.30</td>
                            <td class="align-middle text-center">25.01</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">62.80</td>
                            <td class="align-middle text-center">62.13</td>
                            <td class="align-middle text-center">19.27</td>
                            <td class="align-middle text-center">88.09</td>
                            <td class="align-middle text-center">4.182</td>
                        </tr>

                        <!-- 3s_vs_4z Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">63.89</td>
                            <td class="align-middle text-center">60.49</td>
                            <td class="align-middle text-center">2.92</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">30.63</td>
                            <td class="align-middle text-center">32.05</td>
                            <td class="align-middle text-center">4.182</td>
                            <td class="align-middle text-center">2.57</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">17.20</td>
                            <td class="align-middle text-center">17.45</td>
                            <td class="align-middle text-center">6.02</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">8.55</td>
                            <td class="align-middle text-center">9.21</td>
                            <td class="align-middle text-center">3.10</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">58.75</td>
                            <td class="align-middle text-center">58.63</td>
                            <td class="align-middle text-center">6.24</td>
                            <td class="align-middle text-center">16.95</td>
                            <td class="align-middle text-center">14.86</td>
                        </tr>

                        <!-- 3s_vs_4z Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">69.17</td>
                            <td class="align-middle text-center">59.78</td>
                            <td class="align-middle text-center">4.44</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">47.87</td>
                            <td class="align-middle text-center">41.61</td>
                            <td class="align-middle text-center">5.99</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">34.01</td>
                            <td class="align-middle text-center">29.67</td>
                            <td class="align-middle text-center">4.44</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">7.96</td>
                            <td class="align-middle text-center">7.10</td>
                            <td class="align-middle text-center">5.66</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">60.14</td>
                            <td class="align-middle text-center">60.26</td>
                            <td class="align-middle text-center">7.56</td>
                            <td class="align-middle text-center">3.82</td>
                            <td class="align-middle text-center">19.23</td>
                        </tr>


                        <!-- 3s_vs_5z Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">3s_vs_5z</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">83.08</td>
                            <td class="align-middle text-center">80.30</td>
                            <td class="align-middle text-center">18.27</td>
                            <td class="align-middle text-center">51.27</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">46.93</td>
                            <td class="align-middle text-center">49.09</td>
                            <td class="align-middle text-center">23.09</td>
                            <td class="align-middle text-center">83.86</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">18.31</td>
                            <td class="align-middle text-center">21.25</td>
                            <td class="align-middle text-center">21.64</td>
                            <td class="align-middle text-center">79.40</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">7.15</td>
                            <td class="align-middle text-center">7.62</td>
                            <td class="align-middle text-center">24.22</td>
                            <td class="align-middle text-center">95.95</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">71.08</td>
                            <td class="align-middle text-center">70.51</td>
                            <td class="align-middle text-center">24.07</td>
                            <td class="align-middle text-center">99.21</td>
                            <td class="align-middle text-center">0.8284</td>
                        </tr>

                        <!-- 3s_vs_5z Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">83.97</td>
                            <td class="align-middle text-center">83.42</td>
                            <td class="align-middle text-center">14.41</td>
                            <td class="align-middle text-center">23.59</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">52.49</td>
                            <td class="align-middle text-center">54.76</td>
                            <td class="align-middle text-center">17.29</td>
                            <td class="align-middle text-center">51.18</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">27.64</td>
                            <td class="align-middle text-center">30.78</td>
                            <td class="align-middle text-center">19.96</td>
                            <td class="align-middle text-center">75.02</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">6.79</td>
                            <td class="align-middle text-center">5.60</td>
                            <td class="align-middle text-center">20.84</td>
                            <td class="align-middle text-center">75.14</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">68.75</td>
                            <td class="align-middle text-center">69.60</td>
                            <td class="align-middle text-center">19.80</td>
                            <td class="align-middle text-center">62.08</td>
                            <td class="align-middle text-center">0.7421</td>
                        </tr>

                        <!-- 3s_vs_5z Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">79.11</td>
                            <td class="align-middle text-center">70.92</td>
                            <td class="align-middle text-center">4.97</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">67.05</td>
                            <td class="align-middle text-center">68.42</td>
                            <td class="align-middle text-center">15.08</td>
                            <td class="align-middle text-center">19.77</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">54.04</td>
                            <td class="align-middle text-center">49.80</td>
                            <td class="align-middle text-center">9.78</td>
                            <td class="align-middle text-center">2.23</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">3.39</td>
                            <td class="align-middle text-center">3.39</td>
                            <td class="align-middle text-center">7.68</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">60.70</td>
                            <td class="align-middle text-center">59.62</td>
                            <td class="align-middle text-center">16.41</td>
                            <td class="align-middle text-center">29.18</td>
                            <td class="align-middle text-center">4.571</td>
                        </tr>


                        <!-- 2c_vs_64zg Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">2c_vs_64zg</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">42.57</td>
                            <td class="align-middle text-center">32.92</td>
                            <td class="align-middle text-center">14.19</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">30.90</td>
                            <td class="align-middle text-center">23.84</td>
                            <td class="align-middle text-center">13.27</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">14.59</td>
                            <td class="align-middle text-center">13.84</td>
                            <td class="align-middle text-center">7.57</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">7.38</td>
                            <td class="align-middle text-center">4.98</td>
                            <td class="align-middle text-center">12.90</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">61.17</td>
                            <td class="align-middle text-center">60.56</td>
                            <td class="align-middle text-center">19.15</td>
                            <td class="align-middle text-center">75.00</td>
                            <td class="align-middle text-center">0.5439</td>
                        </tr>

                        <!-- 2c_vs_64zg Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">36.65</td>
                            <td class="align-middle text-center">27.14</td>
                            <td class="align-middle text-center">12.16</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">29.22</td>
                            <td class="align-middle text-center">21.75</td>
                            <td class="align-middle text-center">12.97</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">13.15</td>
                            <td class="align-middle text-center">13.94</td>
                            <td class="align-middle text-center">7.57</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">7.38</td>
                            <td class="align-middle text-center">4.98</td>
                            <td class="align-middle text-center">9.04</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">59.62</td>
                            <td class="align-middle text-center">59.75</td>
                            <td class="align-middle text-center">15.05</td>
                            <td class="align-middle text-center">21.88</td>
                            <td class="align-middle text-center">8.887</td>
                        </tr>

                        <!-- 2c_vs_64zg Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">44.80</td>
                            <td class="align-middle text-center">20.38</td>
                            <td class="align-middle text-center">9.95</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">49.09</td>
                            <td class="align-middle text-center">25.07</td>
                            <td class="align-middle text-center">10.07</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">33.10</td>
                            <td class="align-middle text-center">17.41</td>
                            <td class="align-middle text-center">7.63</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">5.52</td>
                            <td class="align-middle text-center">3.49</td>
                            <td class="align-middle text-center">8.96</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">55.14</td>
                            <td class="align-middle text-center">56.23</td>
                            <td class="align-middle text-center">9.27</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">36.83</td>
                        </tr>


                        <!-- 8m Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">8m</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">67.71</td>
                            <td class="align-middle text-center">52.72</td>
                            <td class="align-middle text-center">14.74</td>
                            <td class="align-middle text-center">44.62</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">57.44</td>
                            <td class="align-middle text-center">52.71</td>
                            <td class="align-middle text-center">19.76</td>
                            <td class="align-middle text-center">96.63</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">21.03</td>
                            <td class="align-middle text-center">19.73</td>
                            <td class="align-middle text-center">15.80</td>
                            <td class="align-middle text-center">53.45</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">11.87</td>
                            <td class="align-middle text-center">11.72</td>
                            <td class="align-middle text-center">19.20</td>
                            <td class="align-middle text-center">90.57</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">64.15</td>
                            <td class="align-middle text-center">64.07</td>
                            <td class="align-middle text-center">19.71</td>
                            <td class="align-middle text-center">96.88</td>
                            <td class="align-middle text-center">0.1596</td>
                        </tr>

                        <!-- 8m Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">63.35</td>
                            <td class="align-middle text-center">57.66</td>
                            <td class="align-middle text-center">12.69</td>
                            <td class="align-middle text-center">18.12</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">65.74</td>
                            <td class="align-middle text-center">69.51</td>
                            <td class="align-middle text-center">16.94</td>
                            <td class="align-middle text-center">63.44</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">25.66</td>
                            <td class="align-middle text-center">49.43</td>
                            <td class="align-middle text-center">10.25</td>
                            <td class="align-middle text-center">3.55</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">11.81</td>
                            <td class="align-middle text-center">12.06</td>
                            <td class="align-middle text-center">17.93</td>
                            <td class="align-middle text-center">78.85</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">63.12</td>
                            <td class="align-middle text-center">64.73</td>
                            <td class="align-middle text-center">19.15</td>
                            <td class="align-middle text-center">90.63</td>
                            <td class="align-middle text-center">1.007</td>
                        </tr>

                        <!-- 8m Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">76.63</td>
                            <td class="align-middle text-center">57.51</td>
                            <td class="align-middle text-center">4.75</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">73.16</td>
                            <td class="align-middle text-center">67.50</td>
                            <td class="align-middle text-center">13.18</td>
                            <td class="align-middle text-center">17.96</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">56.18</td>
                            <td class="align-middle text-center">59.12</td>
                            <td class="align-middle text-center">6.91</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">7.14</td>
                            <td class="align-middle text-center">10.22</td>
                            <td class="align-middle text-center">12.14</td>
                            <td class="align-middle text-center">16.54</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">59.18</td>
                            <td class="align-middle text-center">60.03</td>
                            <td class="align-middle text-center">4.25</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">16.17</td>
                        </tr>


                        <!-- MMM Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">MMM</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">38.99</td>
                            <td class="align-middle text-center">34.49</td>
                            <td class="align-middle text-center">12.16</td>
                            <td class="align-middle text-center">6.56</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">29.93</td>
                            <td class="align-middle text-center">28.78</td>
                            <td class="align-middle text-center">19.65</td>
                            <td class="align-middle text-center">71.85</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">24.11</td>
                            <td class="align-middle text-center">25.61</td>
                            <td class="align-middle text-center">13.01</td>
                            <td class="align-middle text-center">10.07</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">7.38</td>
                            <td class="align-middle text-center">6.97</td>
                            <td class="align-middle text-center">19.47</td>
                            <td class="align-middle text-center">70.42</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">33.28</td>
                            <td class="align-middle text-center">32.72</td>
                            <td class="align-middle text-center">19.09</td>
                            <td class="align-middle text-center">59.00</td>
                            <td class="align-middle text-center">9.669</td>
                        </tr>

                        <!-- MMM Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">49.84</td>
                            <td class="align-middle text-center">42.40</td>
                            <td class="align-middle text-center">10.89</td>
                            <td class="align-middle text-center">5.39</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">34.32</td>
                            <td class="align-middle text-center">32.92</td>
                            <td class="align-middle text-center">15.86</td>
                            <td class="align-middle text-center">37.86</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">34.89</td>
                            <td class="align-middle text-center">35.53</td>
                            <td class="align-middle text-center">9.24</td>
                            <td class="align-middle text-center">1.82</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">8.34</td>
                            <td class="align-middle text-center">8.62</td>
                            <td class="align-middle text-center">15.29</td>
                            <td class="align-middle text-center">34.38</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">33.68</td>
                            <td class="align-middle text-center">32.66</td>
                            <td class="align-middle text-center">15.38</td>
                            <td class="align-middle text-center">45.42</td>
                            <td class="align-middle text-center">5.139</td>
                        </tr>

                        <!-- MMM Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">68.46</td>
                            <td class="align-middle text-center">63.41</td>
                            <td class="align-middle text-center">7.48</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">60.07</td>
                            <td class="align-middle text-center">64.35</td>
                            <td class="align-middle text-center">8.51</td>
                            <td class="align-middle text-center">1.20</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">56.07</td>
                            <td class="align-middle text-center">64.72</td>
                            <td class="align-middle text-center">5.79</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">6.44</td>
                            <td class="align-middle text-center">8.27</td>
                            <td class="align-middle text-center">3.46</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">41.93</td>
                            <td class="align-middle text-center">40.94</td>
                            <td class="align-middle text-center">7.48</td>
                            <td class="align-middle text-center">7.98</td>
                            <td class="align-middle text-center">∞</td>
                        </tr>


                        <!-- bane_vs_bane Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">bane_vs_bane</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">44.08</td>
                            <td class="align-middle text-center">41.77</td>
                            <td class="align-middle text-center">19.31</td>
                            <td class="align-middle text-center">84.06</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">41.65</td>
                            <td class="align-middle text-center">67.23</td>
                            <td class="align-middle text-center">19.85</td>
                            <td class="align-middle text-center">96.07</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">29.34</td>
                            <td class="align-middle text-center">64.71</td>
                            <td class="align-middle text-center">17.42</td>
                            <td class="align-middle text-center">49.48</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">12.73</td>
                            <td class="align-middle text-center">10.65</td>
                            <td class="align-middle text-center">19.44</td>
                            <td class="align-middle text-center">85.02</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">28.21</td>
                            <td class="align-middle text-center">26.31</td>
                            <td class="align-middle text-center">19.99</td>
                            <td class="align-middle text-center">99.54</td>
                            <td class="align-middle text-center">0.0822</td>
                        </tr>

                        <!-- bane_vs_bane Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">64.28</td>
                            <td class="align-middle text-center">37.68</td>
                            <td class="align-middle text-center">18.69</td>
                            <td class="align-middle text-center">65.51</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">40.67</td>
                            <td class="align-middle text-center">43.74</td>
                            <td class="align-middle text-center">18.75</td>
                            <td class="align-middle text-center">74.33</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">24.62</td>
                            <td class="align-middle text-center">40.79</td>
                            <td class="align-middle text-center">15.32</td>
                            <td class="align-middle text-center">24.51</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">0.98</td>
                            <td class="align-middle text-center">1.29</td>
                            <td class="align-middle text-center">18.24</td>
                            <td class="align-middle text-center">59.90</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">29.77</td>
                            <td class="align-middle text-center">28.68</td>
                            <td class="align-middle text-center">19.96</td>
                            <td class="align-middle text-center">98.71</td>
                            <td class="align-middle text-center">0.1326</td>
                        </tr>

                        <!-- bane_vs_bane Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">74.10</td>
                            <td class="align-middle text-center">77.12</td>
                            <td class="align-middle text-center">17.22</td>
                            <td class="align-middle text-center">42.71</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">80.73</td>
                            <td class="align-middle text-center">98.09</td>
                            <td class="align-middle text-center">18.69</td>
                            <td class="align-middle text-center">66.02</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">72.21</td>
                            <td class="align-middle text-center">96.01</td>
                            <td class="align-middle text-center">17.14</td>
                            <td class="align-middle text-center">40.26</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">0.84</td>
                            <td class="align-middle text-center">1.14</td>
                            <td class="align-middle text-center">16.89</td>
                            <td class="align-middle text-center">46.63</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">36.99</td>
                            <td class="align-middle text-center">36.46</td>
                            <td class="align-middle text-center">18.16</td>
                            <td class="align-middle text-center">59.54</td>
                            <td class="align-middle text-center">18.43</td>
                        </tr>


                        <!-- 25m Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">25m</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">58.25</td>
                            <td class="align-middle text-center">51.48</td>
                            <td class="align-middle text-center">13.26</td>
                            <td class="align-middle text-center">20.74</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">50.87</td>
                            <td class="align-middle text-center">49.17</td>
                            <td class="align-middle text-center">19.44</td>
                            <td class="align-middle text-center">87.17</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">33.39</td>
                            <td class="align-middle text-center">34.51</td>
                            <td class="align-middle text-center">13.11</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">2.19</td>
                            <td class="align-middle text-center">1.91</td>
                            <td class="align-middle text-center">16.92</td>
                            <td class="align-middle text-center">38.28</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">48.94</td>
                            <td class="align-middle text-center">47.29</td>
                            <td class="align-middle text-center">19.88</td>
                            <td class="align-middle text-center">96.20</td>
                            <td class="align-middle text-center">0.3219</td>
                        </tr>

                        <!-- 25m Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">59.74</td>
                            <td class="align-middle text-center">51.46</td>
                            <td class="align-middle text-center">13.54</td>
                            <td class="align-middle text-center">7.87</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">59.46</td>
                            <td class="align-middle text-center">50.39</td>
                            <td class="align-middle text-center">13.48</td>
                            <td class="align-middle text-center">2.78</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">48.41</td>
                            <td class="align-middle text-center">47.02</td>
                            <td class="align-middle text-center">12.59</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">1.43</td>
                            <td class="align-middle text-center">1.31</td>
                            <td class="align-middle text-center">18.53</td>
                            <td class="align-middle text-center">60.34</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">46.98</td>
                            <td class="align-middle text-center">45.56</td>
                            <td class="align-middle text-center">19.25</td>
                            <td class="align-middle text-center">84.17</td>
                            <td class="align-middle text-center">18.82</td>
                        </tr>

                        <!-- 25m Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">78.85</td>
                            <td class="align-middle text-center">78.44</td>
                            <td class="align-middle text-center">3.10</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">75.01</td>
                            <td class="align-middle text-center">91.54</td>
                            <td class="align-middle text-center">7.159</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">68.68</td>
                            <td class="align-middle text-center">89.14</td>
                            <td class="align-middle text-center">6.44</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">0.58</td>
                            <td class="align-middle text-center">0.45</td>
                            <td class="align-middle text-center">6.01</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">53.59</td>
                            <td class="align-middle text-center">52.46</td>
                            <td class="align-middle text-center">7.916</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">43.06</td>
                        </tr>


                        <!-- 3s5z Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">3s5z</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">43.48</td>
                            <td class="align-middle text-center">46.07</td>
                            <td class="align-middle text-center">9.39</td>
                            <td class="align-middle text-center">1.46</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">57.61</td>
                            <td class="align-middle text-center">58.45</td>
                            <td class="align-middle text-center">18.90</td>
                            <td class="align-middle text-center">83.70</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">21.98</td>
                            <td class="align-middle text-center">25.76</td>
                            <td class="align-middle text-center">17.18</td>
                            <td class="align-middle text-center">56.53</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">7.43</td>
                            <td class="align-middle text-center">7.68</td>
                            <td class="align-middle text-center">17.85</td>
                            <td class="align-middle text-center">64.39</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">58.54</td>
                            <td class="align-middle text-center">56.88</td>
                            <td class="align-middle text-center">19.28</td>
                            <td class="align-middle text-center">85.88</td>
                            <td class="align-middle text-center">0.5889</td>
                        </tr>

                        <!-- 3s5z Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">63.59</td>
                            <td class="align-middle text-center">56.63</td>
                            <td class="align-middle text-center">12.41</td>
                            <td class="align-middle text-center">7.69</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">62.80</td>
                            <td class="align-middle text-center">56.39</td>
                            <td class="align-middle text-center">17.19</td>
                            <td class="align-middle text-center">58.07</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">30.10</td>
                            <td class="align-middle text-center">26.12</td>
                            <td class="align-middle text-center">16.22</td>
                            <td class="align-middle text-center">39.76</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">6.88</td>
                            <td class="align-middle text-center">7.18</td>
                            <td class="align-middle text-center">14.69</td>
                            <td class="align-middle text-center">28.51</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">57.75</td>
                            <td class="align-middle text-center">56.47</td>
                            <td class="align-middle text-center">16.28</td>
                            <td class="align-middle text-center">51.97</td>
                            <td class="align-middle text-center">110.1</td>
                        </tr>

                        <!-- 3s5z Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">74.59</td>
                            <td class="align-middle text-center">61.77</td>
                            <td class="align-middle text-center">8.55</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">72.86</td>
                            <td class="align-middle text-center">62.50</td>
                            <td class="align-middle text-center">12.82</td>
                            <td class="align-middle text-center">18.22</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">47.08</td>
                            <td class="align-middle text-center">44.29</td>
                            <td class="align-middle text-center">9.72</td>
                            <td class="align-middle text-center">2.13</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">4.20</td>
                            <td class="align-middle text-center">3.43</td>
                            <td class="align-middle text-center">11.34</td>
                            <td class="align-middle text-center">15.85</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">58.66</td>
                            <td class="align-middle text-center">58.62</td>
                            <td class="align-middle text-center">9.96</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">281.7</td>
                        </tr>


                        <!-- MMM2 Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">MMM2</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">63.71</td>
                            <td class="align-middle text-center">61.46</td>
                            <td class="align-middle text-center">8.00</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">43.12</td>
                            <td class="align-middle text-center">42.79</td>
                            <td class="align-middle text-center">12.51</td>
                            <td class="align-middle text-center">18.42</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">25.41</td>
                            <td class="align-middle text-center">26.43</td>
                            <td class="align-middle text-center">9.25</td>
                            <td class="align-middle text-center">1.02</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">17.02</td>
                            <td class="align-middle text-center">17.96</td>
                            <td class="align-middle text-center">9.76</td>
                            <td class="align-middle text-center">3.93</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">53.87</td>
                            <td class="align-middle text-center">53.86</td>
                            <td class="align-middle text-center">18.81</td>
                            <td class="align-middle text-center">75.85</td>
                            <td class="align-middle text-center">44.30</td>
                        </tr>

                        <!-- MMM2 Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">67.85</td>
                            <td class="align-middle text-center">56.71</td>
                            <td class="align-middle text-center">6.89</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">52.28</td>
                            <td class="align-middle text-center">45.35</td>
                            <td class="align-middle text-center">9.02</td>
                            <td class="align-middle text-center">2.34</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">37.52</td>
                            <td class="align-middle text-center">35.53</td>
                            <td class="align-middle text-center">7.94</td>
                            <td class="align-middle text-center">1.07</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">18.59</td>
                            <td class="align-middle text-center">14.06</td>
                            <td class="align-middle text-center">8.32</td>
                            <td class="align-middle text-center">1.67</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">55.00</td>
                            <td class="align-middle text-center">55.31</td>
                            <td class="align-middle text-center">16.25</td>
                            <td class="align-middle text-center">54.95</td>
                            <td class="align-middle text-center">106.8</td>
                        </tr>

                        <!-- MMM2 Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">78.13</td>
                            <td class="align-middle text-center">76.16</td>
                            <td class="align-middle text-center">1.33</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">68.95</td>
                            <td class="align-middle text-center">76.42</td>
                            <td class="align-middle text-center">3.37</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">57.27</td>
                            <td class="align-middle text-center">70.12</td>
                            <td class="align-middle text-center">1.85</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">54.29</td>
                            <td class="align-middle text-center">66.44</td>
                            <td class="align-middle text-center">4.46</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">58.92</td>
                            <td class="align-middle text-center">57.87</td>
                            <td class="align-middle text-center">4.93</td>
                            <td class="align-middle text-center">1.34</td>
                            <td class="align-middle text-center">∞</td>
                        </tr>


                        <!-- 10m_vs_11m Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">10m_vs_11m</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">61.05</td>
                            <td class="align-middle text-center">54.32</td>
                            <td class="align-middle text-center">9.30</td>
                            <td class="align-middle text-center">1.21</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">51.54</td>
                            <td class="align-middle text-center">46.40</td>
                            <td class="align-middle text-center">12.77</td>
                            <td class="align-middle text-center">17.63</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">32.95</td>
                            <td class="align-middle text-center">31.96</td>
                            <td class="align-middle text-center">11.06</td>
                            <td class="align-middle text-center">3.65</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">4.51</td>
                            <td class="align-middle text-center">4.45</td>
                            <td class="align-middle text-center">14.25</td>
                            <td class="align-middle text-center">26.80</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">50.70</td>
                            <td class="align-middle text-center">49.42</td>
                            <td class="align-middle text-center">17.37</td>
                            <td class="align-middle text-center">66.73</td>
                            <td class="align-middle text-center">5.306</td>
                        </tr>

                        <!-- 10m_vs_11m Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">67.87</td>
                            <td class="align-middle text-center">60.18</td>
                            <td class="align-middle text-center">8.86</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">57.84</td>
                            <td class="align-middle text-center">55.31</td>
                            <td class="align-middle text-center">10.88</td>
                            <td class="align-middle text-center">3.48</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">41.74</td>
                            <td class="align-middle text-center">41.99</td>
                            <td class="align-middle text-center">11.71</td>
                            <td class="align-middle text-center">8.86</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">4.61</td>
                            <td class="align-middle text-center">4.54</td>
                            <td class="align-middle text-center">11.63</td>
                            <td class="align-middle text-center">4.60</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">49.58</td>
                            <td class="align-middle text-center">47.58</td>
                            <td class="align-middle text-center">16.22</td>
                            <td class="align-middle text-center">47.91</td>
                            <td class="align-middle text-center">1.790</td>
                        </tr>

                        <!-- 10m_vs_11m Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">81.80</td>
                            <td class="align-middle text-center">77.60</td>
                            <td class="align-middle text-center">4.34</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">72.39</td>
                            <td class="align-middle text-center">87.48</td>
                            <td class="align-middle text-center">6.55</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">61.04</td>
                            <td class="align-middle text-center">71.80</td>
                            <td class="align-middle text-center">2.20</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">3.56</td>
                            <td class="align-middle text-center">2.41</td>
                            <td class="align-middle text-center">6.64</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">57.19</td>
                            <td class="align-middle text-center">54.34</td>
                            <td class="align-middle text-center">4.43</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">∞</td>
                        </tr>


                        <!-- corridor Expert quality -->
                        <tr>
                            <td rowspan="15" class="align-middle text-center">corridor</td>
                            <td rowspan="5" class="align-middle text-center">Expert</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">29.32</td>
                            <td class="align-middle text-center">30.41</td>
                            <td class="align-middle text-center">6.65</td>
                            <td class="align-middle text-center">0.33</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">49.13</td>
                            <td class="align-middle text-center">45.63</td>
                            <td class="align-middle text-center">11.45</td>
                            <td class="align-middle text-center">17.65</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">14.22</td>
                            <td class="align-middle text-center">16.03</td>
                            <td class="align-middle text-center">9.44</td>
                            <td class="align-middle text-center">12.79</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">4.16</td>
                            <td class="align-middle text-center">3.96</td>
                            <td class="align-middle text-center">11.86</td>
                            <td class="align-middle text-center">20.25</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">42.95</td>
                            <td class="align-middle text-center">42.80</td>
                            <td class="align-middle text-center">18.91</td>
                            <td class="align-middle text-center">85.85</td>
                            <td class="align-middle text-center">5.151</td>
                        </tr>

                        <!-- corridor Medium quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Medium</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">43.90</td>
                            <td class="align-middle text-center">39.84</td>
                            <td class="align-middle text-center">1.71</td>
                            <td class="align-middle text-center">1.71</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">50.05</td>
                            <td class="align-middle text-center">47.21</td>
                            <td class="align-middle text-center">8.24</td>
                            <td class="align-middle text-center">16.40</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">21.00</td>
                            <td class="align-middle text-center">26.15</td>
                            <td class="align-middle text-center">3.15</td>
                            <td class="align-middle text-center">0.77</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">3.60</td>
                            <td class="align-middle text-center">3.70</td>
                            <td class="align-middle text-center">6.75</td>
                            <td class="align-middle text-center">3.49</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">43.82</td>
                            <td class="align-middle text-center">43.27</td>
                            <td class="align-middle text-center">15.80</td>
                            <td class="align-middle text-center">56.05</td>
                            <td class="align-middle text-center">41.25</td>
                        </tr>

                        <!-- corridor Poor quality -->
                        <tr>
                            <td rowspan="5" class="align-middle text-center">Poor</td>
                            <td class="align-middle text-center">BC</td>
                            <td class="align-middle text-center">58.02</td>
                            <td class="align-middle text-center">50.92</td>
                            <td class="align-middle text-center">3.01</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">BCQ-MA</td>
                            <td class="align-middle text-center">58.76</td>
                            <td class="align-middle text-center">65.40</td>
                            <td class="align-middle text-center">3.20</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">CQL-MA</td>
                            <td class="align-middle text-center">44.89</td>
                            <td class="align-middle text-center">60.10</td>
                            <td class="align-middle text-center">3.28</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">ICQ-MA</td>
                            <td class="align-middle text-center">2.42</td>
                            <td class="align-middle text-center">2.12</td>
                            <td class="align-middle text-center">3.19</td>
                            <td class="align-middle text-center">0</td>
                            <td class="align-middle text-center">--</td>
                        </tr>
                        <tr>
                            <td class="align-middle text-center">MADT</td>
                            <td class="align-middle text-center">41.41</td>
                            <td class="align-middle text-center">40.43</td>
                            <td class="align-middle text-center">8.83</td>
                            <td class="align-middle text-center">11.08</td>
                            <td class="align-middle text-center">53.18</td>
                        </tr>



                    </tbody>
                </table>
            </div>
        </div>
    </div>

