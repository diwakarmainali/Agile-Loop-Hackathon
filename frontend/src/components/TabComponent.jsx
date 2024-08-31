import React, { useState, useEffect, useCallback } from 'react';
import { FaPlus, FaX } from 'react-icons/fa6';
import { PiRocketLaunch, PiMicrophone, PiStop } from "react-icons/pi";
import axios from 'axios';
import { JsonView, allExpanded, darkStyles } from 'react-json-view-lite';
import 'react-json-view-lite/dist/index.css';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition';
import 'regenerator-runtime/runtime'

const TabComponent = () => {
    const [activeTab, setActiveTab] = useState(0);
    const [tabs, setTabs] = useState([{ id: 0, name: "New Chat", input: "" }]);
    const [jsonResponse, setJsonResponse] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!tabs.find(tab => tab.id === activeTab)) {
            if (tabs.length) {
                setActiveTab(tabs[0].id); // Set to the first tab if there are still tabs
            } else {
                setActiveTab(null); // No tabs left, set activeTab to null
            }
        }
    }, [tabs]);

    const {
        transcript,
        listening,
        resetTranscript,
        browserSupportsSpeechRecognition
    } = useSpeechRecognition();

    useEffect(() => {
        tabs.find(tab => tab.id === activeTab).input = transcript;
    }, [transcript])

    useEffect(() => {
        if (!listening) {
            // append space at the end of the transcript
            tabs.find(tab => tab.id === activeTab).input += ' ';
        }
    }, [listening])
    
    if (!browserSupportsSpeechRecognition) {
        return Alert('Hey quick notes, you cannot do speech to text since your browser does not support it, try to use other browsers :)');
    }

    const addTab = () => {
        const newTab = {
            id: tabs.length ? tabs[tabs.length - 1].id + 1 : 0,
            name: `New Chat`,
            input: ""
        };
        setTabs([...tabs, newTab]);
        setActiveTab(newTab.id);
    };

    const handleInputChange = (id, value) => {
        const updatedTabs = tabs.map(tab =>
            tab.id === id ? { ...tab, input: value } : tab
        );
        setTabs(updatedTabs);
    };

    const removeTab = (id) => {
        const updatedTabs = tabs.filter(tab => tab.id !== id);
        setTabs(updatedTabs);
    };

    const handleSubmit = async () => {
        let activeTabData = tabs.find(tab => tab.id === activeTab);
        
        if (activeTabData && activeTabData.input.trim()) {
            try {
                console.log(_BACKEND_URL_)
                const response = await axios.post(_BACKEND_URL_ + '/api/process-llm-prompt', {
                    prompt: activeTabData.input
                });

                setJsonResponse(response.data);
                setError(null);
                // Clear input after successful submission
                const updatedTabs = tabs.map(tab =>
                    tab.id === activeTab ? { ...tab, input: "" } : tab
                );

                // reset transcript from voice to text
                resetTranscript();
                setTabs(updatedTabs);
            } catch (error) {
                setJsonResponse(null);
                setError('Failed to fetch data');
            }
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            handleSubmit();
        }
    };

    const shouldExpandNode = useCallback(() => true, []);

    return (
        <div className='max-w-7xl mx-auto py-2 px-4 sm:px-6 lg:px-8 flex flex-col md:flex-row gap-10'>
            <div className="pb-4 md:w-[60%] h-[80vh] flex flex-col justify-between bg-[#202020] shadow-md rounded-lg">
                <div className="flex flex-col mb-4">
                    <div className='flex flex-row mb-4 bg-[#0d0d0d] rounded-t-lg'>
                        {tabs.map((tab, index) => (
                            <div key={index} className="flex items-center">
                                <div className={`flex flex-row gap-2 px-4 py-2 rounded-t-lg items-center justify-center 
                                                ${activeTab === tab.id ? 'bg-[#202020] text-gray-400' : 'bg-[#d0d0d0d] text-white'}`}
                                    onClick={() => setActiveTab(tab.id)}
                                >
                                    <p className='font-semibold'>{tab.name}</p>
                                    <button
                                        className="px-2 py-2 text-red-500"
                                        onClick={() => removeTab(tab.id)}
                                    >
                                        <FaX className='h-2 w-2' />
                                    </button>
                                </div>
                            </div>
                        ))}
                        <button
                            className="px-4 py-2 ml-2 text-white rounded"
                            onClick={addTab}
                        >
                            <FaPlus />
                        </button>
                    </div>
                    <div className='flex mx-4 items-center'>
                        <img className="md:block hidden p-2 w-[20vw]" alt="Mask group" src="images/mask-group.png" />
                        <p className='text-xl text-gray-200 font-semibold'>Hi Darel <br /> How can I help you</p>
                    </div>
                </div>

                <div className='bg-[#0d0d0d] flex flex-row gap-2 mx-4 p-4 rounded-lg justify-between'>
                    <div className='flex flex-row gap-2 flex-grow'>
                        {tabs.map(tab => (
                            activeTab === tab.id && (
                                <div key={tab.id} className='flex w-full flex-row'>
                                    <input
                                        type="text"
                                        className="bg-[#0d0d0d] text-gray-200 p-2 w-full outline-none"
                                        value={tab.input}
                                        onChange={(e) => handleInputChange(tab.id, e.target.value)}
                                        onKeyDown={handleKeyDown}
                                        placeholder={`Type your chat prompt here`}
                                    />
                                </div>
                            )
                        ))}
                    </div>
                    <div className='flex flex-row items-center'>
                        {!listening && <PiMicrophone style={{ color: 'white', fontSize: '30px' }} className='w-8 h-10 mx-4' onClick={SpeechRecognition.startListening} /> }
                        {listening && <PiStop style={{ color: 'white', fontSize: '30px' }} className='w-8 h-10 mx-4' onClick={SpeechRecognition.stopListening}/>}
                        <PiRocketLaunch style={{ color: 'white', fontSize: '30px' }} className='w-8 h-10' onClick={handleSubmit} />
                    </div>
                </div>
            </div>
            <div className='p-4 md:w-[40%] bg-[#202020] shadow-md rounded-lg flex items-center justify-center text-gray-300'>
                {error && <p>{error}</p>}
                {jsonResponse ? (
                    <div className='flex items-start rounded-lg'>
                    <JsonView data={jsonResponse} shouldExpandNode={shouldExpandNode} style={darkStyles} />
                    </div>
                ) : (
                    <p>Visualization here</p>
                )}
            </div>
        </div>
    );
};

export default TabComponent;
